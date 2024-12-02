<template>
  <div>
    <h2>Température maximale</h2>
    <canvas id="maxTemperatureChart"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  props: ["station"],
  data() {
    return {
      chart: null,
      chartData: [],
    };
  },
  watch: {
    station: "fetchTemperatureData",
  },
  methods: {
    async fetchTemperatureData() {
      if (!this.station) return;
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/data/max-temperature", {
          params: { station_name: this.station },
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });
        this.chartData = response.data;

        this.renderChart();
      } catch (error) {
        console.error("Erreur lors du chargement des données :", error.response?.data || error.message);
      }
    },
    renderChart() {
      if (this.chart) {
        this.chart.destroy();
      }

      const labels = this.chartData.map((data) => data.date);
      const data = this.chartData.map((data) => data.max_temperature);

      const ctx = document.getElementById("maxTemperatureChart").getContext("2d");
      this.chart = new Chart(ctx, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Température maximale",
              data,
              borderColor: "rgba(255, 99, 132, 1)",
              backgroundColor: "rgba(255, 99, 132, 0.2)",
            },
          ],
        },
      });
    },
  },
  mounted() {
    this.fetchTemperatureData();
  },
};
</script>
