<template>
    <div>
      <h2>Précipitations totales</h2>
      <canvas ref="precipitationCanvas"></canvas>
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
      station: "fetchPrecipitationData",
    },
    methods: {
      async fetchPrecipitationData() {
        if (!this.station) return;
        try {
          const response = await axios.get("http://127.0.0.1:8000/api/data/total-precipitation", {
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
        const data = this.chartData.map((data) => data.total_precipitation);
  
        const ctx = this.$refs.precipitationCanvas.getContext("2d");
        this.chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels,
            datasets: [
              {
                label: "Précipitations totales",
                data,
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1,
              },
            ],
          },
        });
      },
    },
    mounted() {
      this.fetchPrecipitationData();
    },
    beforeUnmount() {
      if (this.chart) {
        this.chart.destroy();
      }
    },
  };
  </script>
  