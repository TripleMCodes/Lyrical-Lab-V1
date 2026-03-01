<script lang="ts">
  import { onMount, onDestroy } from "svelte";
  import Chart from "chart.js/auto";

  let canvas: HTMLCanvasElement;
  let chart: Chart | null = null;

  type Point = { date: string; writing_time: number; sessions: number };

  let data: Point[] = [];
  let days = 30;

  async function load() {
    const res = await fetch(`http://localhost:8000/api/users/dashboard/writing-stats`, {
      credentials: "include"
    });
    if (!res.ok) throw new Error("Failed to load stats");
    data = await res.json();
    console.log(`This is your data ${data}`);
    renderChart();
  }

  function renderChart() {
    const labels = data.map(d => d.date);
    const writingTime = data.map(d => d.writing_time);
    const sessions = data.map(d => d.sessions);

    // destroy existing chart before recreating (avoids duplicates)
    if (chart) chart.destroy();

    chart = new Chart(canvas, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Writing Time",
            data: writingTime,
            yAxisID: "yTime",
            tension: 0.25
          },
          {
            label: "Sessions",
            data: sessions,
            yAxisID: "ySessions",
            tension: 0.25
          }
        ]
      },
      options: {
        responsive: true,
        interaction: { mode: "index", intersect: false },
        scales: {
          yTime: {
            type: "linear",
            position: "left",
            title: { display: true, text: "Writing Time" }
          },
          ySessions: {
            type: "linear",
            position: "right",
            grid: { drawOnChartArea: false },
            title: { display: true, text: "Sessions" }
          }
        }
      }
    });
  }

  onMount(() => {
    load();
  });

  onDestroy(() => {
    if (chart) chart.destroy();
  });
</script>

<div class="card">
  <div class="header">
    <h3>Writing Activity</h3>
  </div>

  <canvas bind:this={canvas}></canvas>
</div>

<style>

  .card { padding: 1rem; border-radius: 12px; background: white; }
  .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; color:black;}
</style>