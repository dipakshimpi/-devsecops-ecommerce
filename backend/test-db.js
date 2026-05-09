const db = require('./config/db');

async function testConnection() {
  console.log('Attempting to connect to PostgreSQL...');
  console.log('Config:', {
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    port: process.env.DB_PORT
  });

  try {
    const res = await db.query('SELECT current_database(), current_user, version()');
    console.log('✅ Connected successfully!');
    console.log('Details:', res.rows[0]);
    
    const tables = await db.query(`
      SELECT table_name 
      FROM information_schema.tables 
      WHERE table_schema = 'public'
    `);
    console.log('Tables in database:', tables.rows.map(r => r.table_name));

    if (!tables.rows.map(r => r.table_name).includes('users')) {
      console.log('❌ Warning: "users" table is MISSING. Did you run init.sql?');
    }
  } catch (err) {
    console.error('❌ Database connection failed!');
    console.error('Error Code:', err.code);
    console.error('Error Message:', err.message);
    if (err.code === '3D000') {
      console.error('Suggestion: The database "ecommerce" does not exist. You need to create it first.');
    } else if (err.code === 'ECONNREFUSED') {
      console.error('Suggestion: PostgreSQL is not running on localhost:5432.');
    } else if (err.code === '28P01') {
      console.error('Suggestion: Invalid password for user "postgres".');
    }
  } finally {
    process.exit();
  }
}

testConnection();
