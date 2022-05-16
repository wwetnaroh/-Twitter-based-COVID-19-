<template>
  <div id="container">
    <Header/>
    <SideBar/>
    <div id="mapContainer"></div>
    <div class="demo-date-picker">
    <div class="block">
      <span class="demonstration">Pick a date</span>
      <el-date-picker @change="changedate" v-model="value" type="date" placeholder="Pick a day" />
    </div>
  </div>
  </div>
</template>

<script>
import Header from './Header.vue'
import SideBar from './SideBar.vue'
import "leaflet/dist/leaflet.css";
import L from "leaflet";
import axios from 'axios'

export default {
  name: 'Map',
  components: {
    Header,SideBar
  },
  data() {
   return{
     center: [37.8, -96],
     value: "",
     layergroup: new L.LayerGroup()
   }
  },
  methods: {
    changedate: function() {
      var date = this.dateform(this.value);
      var filename = "/jsonfile/" + date + ".json"
      console.log(filename)
      axios.get(filename).then(
        res => {
          console.log(res)
          var geojson = L.geoJSON(res.data , {onEachFeature: this.onEachFeature, style: this.styleMap});
          this.layergroup.addLayer(geojson);
        }
      )
    },
    dateform: function(date) {
      var y = date.getFullYear();  
      var m = date.getMonth() + 1;  
      m = m < 10 ? '0' + m : m;  
      var d = date.getDate();  
      d = d < 10 ? ('0' + d) : d;  
      return m + '-' + d + '-' + y; 
    },
    getColor: function (d) {
      return d > 100000 ? '#800026' :
              d > 50000  ? '#BD0026' :
              d > 15000  ? '#E31A1C' :
              d > 5000  ? '#FC4E2A' :
              d > 2000   ? '#FD8D3C' :
              d > 500   ? '#FEB24C' :
              d > 100   ? '#FED976' :
                        '#FFEDA0';
    },
    styleMap: function(feature) {
        return {
            aa: feature,
            fillColor: this.getColor(feature.properties.confirmed),
            fillOpacity: 0.7,
            weight: 1,
            opacity: 1,
            color: 'white',
            dashArray: '2',
        };
    },
    onEachFeature: function(feature, layer) {
      if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name+"<br>"+
        "Confirmed: "+feature.properties.confirmed+"<br>"+
        "death: "+feature.properties.death);
        layer.on('mouseover', () => { layer.openPopup(); });
        layer.on('mouseout', () => { layer.closePopup(); });
      }
    },
    setupLeafletMap: function () {
      const mapDiv = L.map("mapContainer").setView(this.center, 4);
      this.layergroup.addTo(mapDiv)
      L.tileLayer(
        "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
        {
          attribution:
            'Map data (c) <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery (c) <a href="https://www.mapbox.com/">Mapbox</a>',
          maxZoom: 18,
          id: "mapbox/light-v10",
          accessToken:"pk.eyJ1IjoieHlrNTYyNCIsImEiOiJjbDIzemxqZm8xZ2M1M2NxbzcycDFsaTlrIn0.7gO_7xnjpr0aKcp6QWVMdA"
        }
      ).addTo(mapDiv);
   },
 },
 mounted() {
   this.setupLeafletMap();
 },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#container {
  height: 100%
}
#mapContainer {
  margin: 0 auto;
  width: 80vw;
  height: 80vh;
}
.demo-date-picker {
  /* display: flex; */
  width: 100%;
  padding: 0;
  /* flex-wrap: wrap; */
}
.demo-date-picker .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.demo-date-picker .block:last-child {
  border-right: none;
}
.demo-date-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
