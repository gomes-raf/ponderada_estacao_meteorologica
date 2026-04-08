document.addEventListener("DOMContentLoaded", function () {
  const chartCanvas = document.getElementById("chart");
  if (chartCanvas) {
    fetch("/leituras")
      .then((response) => response.json())
      .then((data) => {
        const readings = Array.isArray(data) ? data : data.leituras;
        readings.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        const labels = readings.map((item) =>
          new Date(item.timestamp).toLocaleString(),
        );
        const temperaturas = readings.map((item) => item.temperatura);
        const umidades = readings.map((item) => item.umidade);
        const pressoes = readings.map((item) => item.pressao || null);

        const ctx = chartCanvas.getContext("2d");
        new Chart(ctx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Temperatura (°C)",
                data: temperaturas,
                borderColor: "rgb(255, 99, 132)",
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                yAxisID: "y",
              },
              {
                label: "Umidade (%)",
                data: umidades,
                borderColor: "rgb(54, 162, 235)",
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                yAxisID: "y",
              },
              {
                label: "Pressão (hPa)",
                data: pressoes,
                borderColor: "rgb(75, 192, 192)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                yAxisID: "y1",
              },
            ],
          },
          options: {
            responsive: true,
            interaction: {
              mode: "index",
              intersect: false,
            },
            stacked: false,
            plugins: {
              title: {
                display: true,
                text: "Variação Temporal das Leituras",
              },
            },
            scales: {
              y: {
                type: "linear",
                display: true,
                position: "left",
              },
              y1: {
                type: "linear",
                display: true,
                position: "right",
                grid: {
                  drawOnChartArea: false,
                },
              },
            },
          },
        });
      })
      .catch((error) => {
        console.error("Erro ao carregar dados para o gráfico:", error);
      });
  }

  const lastReadingsContainer = document.getElementById(
    "last-readings-container",
  );
  const refreshButton = document.getElementById("refresh-button");
  const historyBody = document.getElementById("history-body");
  const pageInfo = document.getElementById("page-info");
  const prevButton = document.getElementById("page-prev");
  const nextButton = document.getElementById("page-next");

  function loadLastReadings() {
    if (!lastReadingsContainer) return;
    fetch("/leituras")
      .then((response) => response.json())
      .then((data) => {
        const readings = Array.isArray(data) ? data : data.leituras;
        if (!readings || readings.length === 0) {
          lastReadingsContainer.innerHTML =
            "<p>Nenhuma leitura registrada ainda.</p>";
          return;
        }
        const last5 = readings.slice(-5).reverse();
        const html = last5
          .map(
            (leitura) => `
                    <div class="reading-card">
                        <h3>Leitura ${leitura.id}</h3>
                        <p><strong>Temperatura:</strong> ${leitura.temperatura}°C</p>
                        <p><strong>Umidade:</strong> ${leitura.umidade}%</p>
                        <p><strong>Pressão:</strong> ${leitura.pressao || "N/A"} hPa</p>
                        <p><strong>Timestamp:</strong> ${new Date(leitura.timestamp).toLocaleString()}</p>
                    </div>
                `,
          )
          .join("");
        lastReadingsContainer.innerHTML = html;
      })
      .catch((error) => {
        console.error("Erro ao carregar últimas leituras:", error);
        lastReadingsContainer.innerHTML = "<p>Erro ao carregar leituras.</p>";
      });
  }

  if (refreshButton) {
    refreshButton.addEventListener("click", loadLastReadings);
  }

  loadLastReadings();

  let currentPage = 1;
  const pageLimit = 10;
  let totalReadings = 0;

  function renderHistoryPage(data) {
    const readings = Array.isArray(data) ? data : data.leituras;
    totalReadings = data.total || readings.length;
    if (!historyBody) return;

    if (!readings || readings.length === 0) {
      historyBody.innerHTML =
        '<tr><td colspan="6">Nenhuma leitura registrada ainda.</td></tr>';
      return;
    }

    historyBody.innerHTML = readings
      .map(
        (leitura) => `
            <tr>
                <td>${leitura.id}</td>
                <td>${leitura.temperatura}</td>
                <td>${leitura.umidade}</td>
                <td>${leitura.pressao || "-"}</td>
                <td>${leitura.timestamp}</td>
                <td class="actions-cell">
                    <a class="link-button" href="/editar/${leitura.id}">Editar</a>
                    <form action="/deletar/${leitura.id}" method="post" class="inline-form">
                        <button type="submit" class="danger">Excluir</button>
                    </form>
                </td>
            </tr>
        `,
      )
      .join("");

    const totalPages = Math.max(1, Math.ceil(totalReadings / pageLimit));
    if (pageInfo) {
      pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
    }
    if (prevButton) {
      prevButton.disabled = currentPage <= 1;
    }
    if (nextButton) {
      nextButton.disabled = currentPage >= totalPages;
    }
  }

  function loadHistoryPage(page) {
    if (!historyBody) return;
    fetch(`/leituras?page=${page}&limit=${pageLimit}`)
      .then((response) => response.json())
      .then((data) => {
        currentPage = page;
        renderHistoryPage(data);
      })
      .catch((error) => {
        console.error("Erro ao carregar página do histórico:", error);
      });
  }

  if (prevButton) {
    prevButton.addEventListener("click", () => {
      if (currentPage > 1) {
        loadHistoryPage(currentPage - 1);
      }
    });
  }

  if (nextButton) {
    nextButton.addEventListener("click", () => {
      loadHistoryPage(currentPage + 1);
    });
  }

  if (historyBody) {
    loadHistoryPage(currentPage);
  }

  const editForm = document.getElementById("edit-reading-form");
  if (editForm) {
    editForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const leituraId = editForm.dataset.id;
      const temperatura = document.getElementById("temperatura").value;
      const umidade = document.getElementById("umidade").value;
      const pressao = document.getElementById("pressao").value || null;

      fetch(`/leituras/${leituraId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          temperatura,
          umidade,
          pressao,
        }),
      })
        .then((response) => {
          if (response.ok) {
            window.location.href = "/historico";
          } else {
            return response.json().then((data) => {
              throw new Error(data.erro || "Erro ao atualizar leitura");
            });
          }
        })
        .catch((error) => {
          alert(`Falha na atualização: ${error.message}`);
        });
    });
  }
});
