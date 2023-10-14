use actix_web::{get, web, App, HttpResponse, HttpServer, Responder};
use dotenv::dotenv;
use serde::{Deserialize, Serialize};
use serde_json;
use sqlx::postgres::{PgPool, PgPoolOptions};

pub struct AppState {
    db: PgPool,
}

#[derive(Debug, Deserialize, Serialize, sqlx::FromRow)]
#[allow(non_snake_case)]
pub struct AyatShort {
    pub public_id: String,
    pub sura_id: Option<i32>,
    pub ayat_number: String,
    pub day: Option<i32>,
}

#[derive(Deserialize, Debug)]
pub struct PaginationOptions {
    pub page: Option<usize>,
    pub page_size: Option<usize>,
}

#[get("/api/v1/ayats")]
async fn ayats_list(
    opts: web::Query<PaginationOptions>,
    data: web::Data<AppState>,
) -> impl Responder {
    let page_num = opts.page.unwrap_or(1);
    let page_size = opts.page_size.unwrap_or(50);
    let offset = (page_num - 1) * page_size;
    let count: (i64,) = sqlx::query_as("SELECT COUNT(*) FROM ayats")
        .fetch_one(&data.db)
        .await
        .unwrap();
    let ayats: Vec<AyatShort> = sqlx::query_as!(
        AyatShort,
        "SELECT \
          public_id, \
          sura_id, \
          ayat_number, \
          day \
        FROM ayats \
        ORDER BY ayat_id \
        OFFSET $1 \
        LIMIT $2",
        offset as i32,
        page_size as i32
    )
    .fetch_all(&data.db)
    .await
    .unwrap();
    let json_response = serde_json::json!({
        "count": count,
        "prev": 0,
        "next": page_num + 1,
        "results": ayats
    });
    HttpResponse::Ok().json(json_response)
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv().ok();
    let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    let pool = match PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
    {
        Ok(pool) => {
            println!("Connection to the database is successful!");
            pool
        }
        Err(err) => {
            println!("Failed to connect to the database: {:?}", err);
            std::process::exit(1);
        }
    };
    println!("Server started successfully");
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(AppState { db: pool.clone() }))
            .service(ayats_list)
    })
    .bind(("0.0.0.0", 8010))?
    .run()
    .await
}
