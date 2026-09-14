# Analytics FastAPI (Aiven)

> 📌 **Project Note:** This repository is a *fork* of the original project created by [Coding For Entrepreneurs](https://github.com/codingforentrepreneurs/analytics-api). 
> 
> I have made some  modifications to adapt the environment. The original version utilizes **Docker** containers, whereas this variant has been migrated to connect natively to **Aiven** cloud-managed services using timescaledb extension of Aiven. Also Render was use to deploy the app instead of Railway. The application of hypertable was done using SQL inside the code (session.py) to convert the SQLModel table to hypertable. Aiven free service doesn't allow some of the properties of timescaledb.The drop_after function is not available, so the chunk drops was manually setted inside Aiven with pg_cron extension

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
CREATE EXTENSION IF NOT EXISTS pg_cron CASCADE;

-- Create an automated schedule inside Aiven to remove chunks after 1 month
SELECT cron.schedule(
    'chunk clean',
    '0 0 * * *',
    $$ SELECT drop_chunks('public.eventmodel', INTERVAL '1 month') $$ 
);
```



