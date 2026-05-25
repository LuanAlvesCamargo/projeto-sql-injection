// ============================================================
// script.js - VERSÃO VULNERÁVEL
// Scripts de interface e demonstração de SQL Injection
// ============================================================

// ── Auto-fechar alertas após 4s ─────────────────────────────
document.addEventListener("DOMContentLoaded", function () {
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.transition = "opacity .5s";
      alert.style.opacity = "0";
      setTimeout(function () { alert.remove(); }, 500);
    }, 4000);
  });
});

// ── Confirmar exclusão ──────────────────────────────────────
function confirmDelete(bookTitle) {
  return confirm(`Deseja realmente excluir o livro:\n"${bookTitle}"?`);
}

// ── Preencher payload de SQL Injection no login ─────────────
function fillSQLInjection(type) {
  const user = document.getElementById("username");
  const pass = document.getElementById("password");
  if (!user || !pass) return;

  const payloads = {
    bypass:  { u: "' OR '1'='1", p: "' OR '1'='1" },
    comment: { u: "admin'--",    p: "qualquer_coisa"  },
    union:   { u: "' UNION SELECT 1,2,3,4,5--", p: "x" },
  };

  const p = payloads[type];
  if (p) {
    user.value = p.u;
    pass.value = p.p;
    user.style.borderColor = "#e63946";
    pass.style.borderColor = "#e63946";
  }
}

// ── Highlight da query exibida na tela ──────────────────────
function highlightSQL(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;

  let text = el.textContent;

  const keywords = ["SELECT", "FROM", "WHERE", "AND", "OR", "LIKE",
                    "INSERT", "UPDATE", "DELETE", "UNION", "INTO", "--"];
  keywords.forEach(function (kw) {
    const re = new RegExp("\\b" + kw + "\\b", "g");
    text = text.replace(re, `<span style="color:#f4a261;font-weight:700">${kw}</span>`);
  });

  el.innerHTML = text;
}
