/* eslint-disable no-console */
// 统一后端：fCC 质量保证 / 信息安全 5 个项目的 API（内存存储）
const path = require("path");
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors({ origin: "*" }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const PORT = process.env.PORT || 3000;

app.use("/qa", express.static(path.join(__dirname, "..", "qa-projects")));

// ---------------------------------------------------------------- 通用工具
function nextId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 10);
}

function isoNow() {
  return new Date().toISOString();
}

// ------------------------------------------------- 1. 公制 / 英制转换器
const METRIC_UNITS = {
  gal: { name: "gallon", plural: "gallons", metric: "L", factor: (v) => v * 3.78541 },
  l: { name: "liter", plural: "liters", metric: "gal", factor: (v) => v / 3.78541 },
  lbs: { name: "pound", plural: "pounds", metric: "kg", factor: (v) => v * 0.453592 },
  kg: { name: "kilogram", plural: "kilograms", metric: "lbs", factor: (v) => v / 0.453592 },
  mi: { name: "mile", plural: "miles", metric: "km", factor: (v) => v * 1.60934 },
  km: { name: "kilometer", plural: "kilometers", metric: "mi", factor: (v) => v / 1.60934 }
};

const UNIT_LABEL = {
  gal: { name: "gallon", plural: "gallons" },
  L: { name: "liter", plural: "liters" },
  lbs: { name: "pound", plural: "pounds" },
  kg: { name: "kilogram", plural: "kilograms" },
  mi: { name: "mile", plural: "miles" },
  km: { name: "kilometer", plural: "kilometers" }
};

function parseNumber(raw) {
  if (raw === undefined || raw === null || raw === "") return 1;
  if (raw.includes("/")) {
    const parts = raw.split("/");
    if (parts.length !== 2) return NaN;
    const numerator = Number(parts[0]);
    const denominator = Number(parts[1]);
    if (!Number.isFinite(numerator) || !Number.isFinite(denominator) || denominator === 0) return NaN;
    return numerator / denominator;
  }
  const value = Number(raw);
  return Number.isFinite(value) ? value : NaN;
}

function round5(value) {
  return Math.round(value * 100000) / 100000;
}

app.get("/api/convert", (req, res) => {
  const input = String(req.query.input || "").trim();
  if (!input) return res.json("invalid input");

  const match = input.match(/^([+-]?\d*\.?\d+(?:\/[+-]?\d*\.?\d+)?)?\s*([a-zA-Z]+)$/);
  if (!match) return res.json("invalid input");

  const rawNumber = match[1] || "";
  const rawUnit = match[2] || "";
  const unitKey = rawUnit === "L" || rawUnit === "l" ? "l" : rawUnit.toLowerCase();

  if (rawNumber.includes("/")) {
    const pieces = rawNumber.split("/");
    if (pieces.length !== 2 || pieces[0] === "" || pieces[1] === "") return res.json("invalid number");
    const num = Number(pieces[0]);
    const den = Number(pieces[1]);
    if (!Number.isFinite(num) || !Number.isFinite(den) || den === 0) return res.json("invalid number");
  }

  const initNum = parseNumber(rawNumber);
  if (!Number.isFinite(initNum)) return res.json("invalid number");

  const unit = METRIC_UNITS[unitKey];
  if (!unit) return res.json("invalid unit");

  const returnNum = round5(unit.factor(initNum));
  const returnUnit = unit.metric;
  const fromLabel = UNIT_LABEL[unitKey] || { name: unitKey, plural: unitKey };
  const toLabel = UNIT_LABEL[returnUnit];
  const fromWord = initNum === 1 ? fromLabel.name : fromLabel.plural;
  const toWord = returnNum === 1 ? toLabel.name : toLabel.plural;

  res.json({
    initNum,
    initUnit: unitKey === "l" ? "L" : unitKey,
    returnNum,
    returnUnit,
    string: initNum + " " + fromWord + " converts to " + returnNum + " " + toWord
  });
});

// ------------------------------------------------------- 2. 问题跟踪器
const issueProjects = new Map();

function getIssueProject(name) {
  if (!issueProjects.has(name)) issueProjects.set(name, []);
  return issueProjects.get(name);
}

app
  .route("/api/issues/:project")
  .get((req, res) => {
    const issues = getIssueProject(req.params.project);
    const filters = req.query || {};
    const filtered = issues.filter((issue) =>
      Object.entries(filters).every(([key, value]) => String(issue[key]) === String(value))
    );
    res.json(filtered);
  })
  .post((req, res) => {
    const { issue_title, issue_text, created_by, assigned_to, status_text } = req.body || {};
    if (!issue_title || !issue_text || !created_by) {
      return res.json({ error: "missing inputs" });
    }
    const timestamp = isoNow();
    const issue = {
      _id: nextId(),
      issue_title,
      issue_text,
      created_by,
      assigned_to: assigned_to || "",
      status_text: status_text || "Open",
      created_on: timestamp,
      updated_on: timestamp,
      open: true
    };
    getIssueProject(req.params.project).push(issue);
    res.json(issue);
  })
  .put((req, res) => {
    const { _id, ...fields } = req.body || {};
    if (!_id) return res.json({ error: "_id error" });
    const issues = getIssueProject(req.params.project);
    const issue = issues.find((item) => item._id === _id);
    if (!issue) return res.json({ error: "could not update " + _id });

    const updates = Object.entries(fields).filter(([key]) => key in issue);
    if (updates.length === 0) return res.json({ error: "no updated field sent" });

    for (const [key, value] of updates) {
      issue[key] = key === "open" ? value === true || value === "true" : value;
    }
    issue.updated_on = isoNow();
    res.json({ result: "successfully updated" });
  })
  .delete((req, res) => {
    const id = (req.body || {}).issue_id || (req.body || {})._id;
    if (!id) return res.json({ error: "_id error" });
    const issues = getIssueProject(req.params.project);
    const index = issues.findIndex((item) => item._id === id);
    if (index === -1) return res.json({ error: "could not delete " + id });
    issues.splice(index, 1);
    res.json({ result: "deleted " + id });
  });

// ---------------------------------------------------------- 3. 个人图书库
const books = [];

app
  .route("/api/books")
  .get((req, res) => {
    res.json(books.map((book) => ({
      _id: book._id,
      title: book.title,
      commentcount: book.comments.length
    })));
  })
  .post((req, res) => {
    const title = (req.body || {}).title;
    if (!title) return res.json("missing title");
    const book = { _id: nextId(), title, comments: [] };
    books.push(book);
    res.json({ _id: book._id, title: book.title, comments: [] });
  });

app
  .route("/api/books/:id")
  .get((req, res) => {
    const book = books.find((item) => item._id === req.params.id);
    if (!book) return res.json("no book exists");
    res.json(book);
  })
  .post((req, res) => {
    const comment = (req.body || {}).comment;
    const book = books.find((item) => item._id === req.params.id);
    if (!book) return res.json("no book exists");
    if (!comment) return res.json("missing comment");
    book.comments.push(comment);
    res.json(book);
  })
  .delete((req, res) => {
    const index = books.findIndex((item) => item._id === req.params.id);
    if (index === -1) return res.json("could not delete");
    books.splice(index, 1);
    res.json("deleted " + req.params.id);
  });

// ------------------------------------------------------ 4. 股票价格检查器
const stockLikes = new Map();
const PROXY_BASE = "https://stock-price-checker-proxy.freecodecamp.rocks/v1/stock/";

async function fetchPrice(symbol) {
  const response = await fetch(PROXY_BASE + encodeURIComponent(symbol) + "/quote");
  if (!response.ok) throw new Error("quote failed");
  const data = await response.json();
  if (!data || typeof data.latestPrice !== "number") throw new Error("no price");
  return { stock: String(data.symbol || symbol).toUpperCase(), price: data.latestPrice };
}

app.get("/api/stock-prices", async (req, res) => {
  const rawStocks = req.query.stock;
  const like = req.query.like === "true" || req.query.like === true;
  const clientKey = req.ip || "anonymous";

  if (!rawStocks) return res.json("stock required");

  const symbols = (Array.isArray(rawStocks) ? rawStocks : [rawStocks])
    .map((symbol) => String(symbol).toUpperCase())
    .filter(Boolean)
    .slice(0, 2);

  try {
    const quotes = await Promise.all(symbols.map((symbol) => fetchPrice(symbol)));

    if (like) {
      for (const quote of quotes) {
        if (!stockLikes.has(quote.stock)) stockLikes.set(quote.stock, new Set());
        const set = stockLikes.get(quote.stock);
        if (!set.has(clientKey)) set.add(clientKey);
      }
    }

    if (quotes.length === 2) {
      const [first, second] = quotes;
      const firstLikes = (stockLikes.get(first.stock) || new Set()).size;
      const secondLikes = (stockLikes.get(second.stock) || new Set()).size;
      return res.json({
        stockData: [
          { stock: first.stock, price: first.price, rel_likes: firstLikes - secondLikes },
          { stock: second.stock, price: second.price, rel_likes: secondLikes - firstLikes }
        ]
      });
    }

    const quote = quotes[0];
    res.json({
      stockData: {
        stock: quote.stock,
        price: quote.price,
        likes: (stockLikes.get(quote.stock) || new Set()).size
      }
    });
  } catch (error) {
    res.json({ error: "external source error" });
  }
});

// ------------------------------------------------------ 5. 匿名留言板
const boards = new Map();

function getBoard(name) {
  if (!boards.has(name)) boards.set(name, []);
  return boards.get(name);
}

function publicReply(reply) {
  return {
    _id: reply._id,
    text: reply.reported ? "[reported]" : reply.text,
    created_on: reply.created_on
  };
}

function publicThread(thread, replyLimit) {
  const sortedReplies = [...thread.replies].sort((a, b) => new Date(b.created_on) - new Date(a.created_on));
  const replies = replyLimit ? sortedReplies.slice(0, replyLimit) : sortedReplies;
  return {
    _id: thread._id,
    text: thread.reported ? "[reported]" : thread.text,
    created_on: thread.created_on,
    bumped_on: thread.bumped_on,
    replies: replies.map(publicReply),
    replycount: thread.replies.length,
    reported: thread.reported
  };
}

app
  .route("/api/threads/:board")
  .get((req, res) => {
    const threads = [...getBoard(req.params.board)]
      .sort((a, b) => new Date(b.bumped_on) - new Date(a.bumped_on))
      .slice(0, 10);
    res.json(threads.map((thread) => publicThread(thread, 3)));
  })
  .post((req, res) => {
    const { text, delete_password } = req.body || {};
    if (!text || !delete_password) return res.json({ error: "missing fields" });
    const timestamp = isoNow();
    const thread = {
      _id: nextId(),
      text,
      delete_password,
      created_on: timestamp,
      bumped_on: timestamp,
      reported: false,
      replies: []
    };
    getBoard(req.params.board).push(thread);
    res.json(thread);
  })
  .put((req, res) => {
    const { thread_id, delete_password, report_id } = req.body || {};
    if (!thread_id) return res.json({ error: "thread_id error" });
    const board = getBoard(req.params.board);
    const thread = board.find((item) => item._id === thread_id);
    if (!thread) return res.json({ error: "thread not found" });

    if (report_id) {
      thread.reported = true;
      return res.send("reported");
    }
    if (thread.delete_password !== delete_password) return res.send("incorrect password");
    const index = board.indexOf(thread);
    board.splice(index, 1);
    res.send("success");
  });

app
  .route("/api/replies/:board")
  .get((req, res) => {
    const thread = getBoard(req.params.board).find((item) => item._id === req.query.thread_id);
    if (!thread) return res.json({ error: "thread not found" });
    res.json(publicThread(thread, 0));
  })
  .post((req, res) => {
    const { thread_id, text, delete_password } = req.body || {};
    if (!thread_id || !text || !delete_password) return res.json({ error: "missing fields" });
    const thread = getBoard(req.params.board).find((item) => item._id === thread_id);
    if (!thread) return res.json({ error: "thread not found" });
    const timestamp = isoNow();
    thread.replies.push({
      _id: nextId(),
      text,
      delete_password,
      created_on: timestamp,
      reported: false
    });
    thread.bumped_on = timestamp;
    res.json(publicThread(thread, 0));
  })
  .put((req, res) => {
    const { thread_id, reply_id, delete_password, report_id } = req.body || {};
    if (!thread_id || !reply_id) return res.json({ error: "id error" });
    const thread = getBoard(req.params.board).find((item) => item._id === thread_id);
    if (!thread) return res.json({ error: "thread not found" });
    const reply = thread.replies.find((item) => item._id === reply_id);
    if (!reply) return res.json({ error: "reply not found" });

    if (report_id) {
      reply.reported = true;
      return res.send("reported");
    }
    if (reply.delete_password !== delete_password) return res.send("incorrect password");
    thread.replies = thread.replies.filter((item) => item._id !== reply_id);
    res.send("success");
  });

app.get("/", (req, res) => {
  res.type("html").send(
    "<h1>fCC Backend</h1><p>APIs: /api/convert, /api/issues/:project, /api/books, /api/stock-prices, /api/threads/:board, /api/replies/:board</p>"
  );
});

app.listen(PORT, () => {
  console.log("fcc backend listening on " + PORT);
});
