function renumerar() {
    document.querySelectorAll('.card.item').forEach((li, i) => {
        const num = li.querySelector('.number');
        if (num) num.textContent = (i + 1) + '.';
    });
}


addEventListener('click', e => {
    const btn = e.target.closest('[data-action="toggle"]');
    if (btn) {
        const li = btn.closest('[data-id]');
        const id = li?.dataset?.id;
        if (!id) return;
        fetch(`/items/${id}/toggle`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'fetch' }
        })
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    li.classList.toggle('done');
                    btn.textContent = d.done ? '✔' : '○';
                }
            });
        return;
    }


    const delBtn = e.target.closest('form[action^="/items/"][method="post"] button.icon-btn.danger');
    if (delBtn) {
        e.preventDefault();
        const form = delBtn.closest('form');
        const li = delBtn.closest('[data-id]');
        const id = li?.dataset?.id;
        if (!id || !confirm('Eliminar ítem?')) return;
        fetch(`/items/${id}/delete`, {
            method: 'POST',
            headers: { 'X-Requested-With': 'fetch' }
        })
            .then(r => r.json())
            .then(d => {
                if (d.ok) {
                    li.remove();
                    renumerar();
                }
            });
    }
});


window.addEventListener('DOMContentLoaded', renumerar);