// ============================================================
// script.js - VERSÃO SEGURA
// Scripts de interface — sem helpers de ataque
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
