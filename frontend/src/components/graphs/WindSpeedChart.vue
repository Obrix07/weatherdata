<template>
    <div>
      <h2>Vitesse maximale du vent</h2>
      <canvas ref="windSpeedCanvas"></canvas>
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
      station: "fetchWindSpeedData",
    },
    methods: {
      async fetchWindSpeedData() {
        if (!this.station) return;
        try {
          const response = await axios.get("http://127.0.0.1:8000/api/data/max-wind-speed", {
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
        const data = this.chartData.map((data) => data.max_wind_speed);
  
        const ctx = this.$refs.windSpeedCanvas.getContext("2d");
        this.chart = new Chart(ctx, {
          type: "line",
          data: {
            labels,
            datasets: [
              {
                label: "Vitesse maximale du vent",
                data,
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                pointRadius: 2,
              },
            ],
          },
        });
      },
    },
    mounted() {
      this.fetchWindSpeedData();
    },
    beforeUnmount() {
      if (this.chart) {
        this.chart.destroy();
      }
    },
  };
  </script>
  