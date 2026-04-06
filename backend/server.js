const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const crypto = require("crypto");

const app = express();
app.use(express.json());
app.use(cors());

const db = new sqlite3.Database("./db.sqlite");

// 建表
db.run(`
CREATE TABLE IF NOT EXISTS users (
  serial TEXT PRIMARY KEY,
  name TEXT
)
`);

// 預設一組序號（你可以自己改）
db.run(`INSERT OR IGNORE INTO users VALUES ('ABC123456789XYZ','VIP用戶')`);

// 登入
app.post("/validate", (req, res) => {
  const { serial } = req.body;

  db.get("SELECT * FROM users WHERE serial=?", [serial], (err, row) => {
    if (!row) return res.json({ ok: false, msg: "序號錯誤" });

    return res.json({
      ok: true,
      token: Date.now(),
      user: row.name
    });
  });
});

// 預測（簡化版）
app.post("/predict", (req, res) => {
  const r = Math.random() > 0.5 ? "莊" : "閒";

  res.json({
    ok: true,
    result: r
  });
});

app.listen(3000, () => console.log("API running"));
