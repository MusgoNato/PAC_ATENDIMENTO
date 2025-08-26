
/*-------------Totem do usuario-------------*/
async function takeTicket(category){
      try {
        const res = await fetch('/api/tickets', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category })
        });

        if(!res.ok){
          alert('Senha nao implementada!');
          return;
        }
        const t = await res.json();
        const when = new Date(t.created_at);
        const info = `${t.category} • Nº ${t.number} • ${when.toLocaleString()}`;
        document.getElementById('ticketCode').textContent = t.code;
        document.getElementById('ticketInfo').textContent = info;
        document.getElementById('ticketModal').style.display = 'grid';
        document.getElementById('printCode').textContent = t.code;
        document.getElementById('printMeta').textContent = info;
      } catch(e){ alert('Falha de conexão.'); }
    }

    function closeModal(){
      document.getElementById('ticketModal').style.display = 'none';
    }

    function printTicket(){
      const area = document.getElementById('printArea');
      area.style.display = 'block';
      window.print();
      setTimeout(() => area.style.display = 'none', 100);
    }
/*-------------Totem do usuario-------------*/