document.addEventListener('DOMContentLoaded', function() {
    fetch('/api2/automobiliai') // Endpoint'ą pakeičiau į automobilius
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('automobiliai-body');
            if (!tbody) return; // Patikrinimas, ar elementas egzistuoja

            tbody.innerHTML = '';

            data.forEach(automobilis => {
                const tr = document.createElement('tr');

                tr.innerHTML = `
                    <td>${automobilis.gamintojas}</td>
                    <td>${automobilis.modelis}</td>
                    <td>${automobilis.spalva}</td>
                    <td>${automobilis.metai}</td>
                    <td>${automobilis.kaina} €</td>
                `;

                tbody.appendChild(tr);
            });
        })
        .catch(error => console.error('Klaida gaunant duomenis:', error));
});