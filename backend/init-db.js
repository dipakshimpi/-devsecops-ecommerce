const fs = require('fs');
const path = require('path');
const db = require('./config/db');

async function initDB() {
  console.log('Reading init.sql...');
  const sqlPath = path.join(__dirname, '../database/init.sql');
  const sql = fs.readFileSync(sqlPath, 'utf8');

  try {
    console.log('Executing SQL... This will create tables and seed products.');
    await db.query(sql);
    console.log('✅ Database initialized successfully!');
  } catch (err) {
    console.error('❌ Error initializing database:', err.message);
  } finally {
    process.exit();
  }
}

initDB();
