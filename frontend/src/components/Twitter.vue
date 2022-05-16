<template>
  <div id="container">
    <Header />
    <SideBar />
    <h2 style="overflow: hidden; max-width:400px; margin: 0 auto;">Top Trending Twitter Hashtags</h2>
    <div style="overflow: hidden; width: 90%; margin: 0 auto;">
      <div style="display: inline-block;width: 45%; margin-bottom:50px"><vue3-chart-js ref="chart" v-bind="{ ...chart_config }" /></div>
      <div style="display: inline-block;width: 45%;"><Cloud /></div>
      
    </div>
    
  </div>
</template>

<script>
import Header from './Header.vue'
import SideBar from './SideBar.vue'
import Cloud from './WordCloud.vue'
import Vue3ChartJs from "@j-t-mcc/vue3-chartjs"
import axios from 'axios'

export default {
  name: 'Twitter',
  components: {
    Header,SideBar,Vue3ChartJs,Cloud
  },
  data() {
   return{
     labels: [1],
     values: [],
     chart: "",
     chart_config: {}
   }
  },
  methods: {
    init_chart_config: function(){
      this.chart_config = {
        type: 'bar',
        data: {
          labels: [],
          datasets: [{
            label: '# of Mentions',
            data: [],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)',
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
              'rgba(255,99,132,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
              'rgba(255,99,132,1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1
          }]
        },
        options: {
          indexAxis: 'y',
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
    }
   }
 },
 created() {
   this.init_chart_config()
   setInterval(() => {
      axios.get('http://localhost:5001/refreshData').then(res => {
        this.chart_config.data.labels = res.data.sLabel
        this.chart_config.data.datasets[0].data = res.data.sData
        this.$refs.chart.update(250)
      }).catch(() => {
        // console.log(this.$refs.chart)
      })
  },1000);
 },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#container {
  height: 100%;
}
#mapContainer {
  margin-left: 10%;
  width: 50vw;
  height: 50vh;
}
</style>
