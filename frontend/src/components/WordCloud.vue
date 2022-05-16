<template>
  <div id="wc">
      <!-- <wordcloud
      :data="defaultWords"
      nameKey="name"
      valueKey="value"
      color="Accent">
      </wordcloud> -->
  </div>
</template>


<script>
import axios from 'axios'
import * as d3 from 'd3'
import * as cloud from 'd3-cloud'

export default {
  name: 'cloud',
  data() {
   return{
    src_Label_Data: [],
    src_Labels: [], 
    src_Data: [],
    fill: [],
    c: "",
   }
  },
  methods: {
    wordClickHandler(name, value, vm) {
      console.log('wordClickHandler', name, value, vm);
    },
    findsum: function() {
      var sum = 0;
      for(var i=0,len=this.src_Data.length; i<len; i++){
          sum += this.src_Data[i];
          //console.log(sum);
      }
      return sum;
    },
    draw: function(word) {
      console.log('I am in draw')
      d3.select("#wc").append("svg")
          .attr("width", 750)
          .attr("height", 500)
          .append("g")
          .attr("transform", "translate(375,250)")
          .selectAll("text")
          .data(word)
          .enter().append("text")
          .style("font-size", function(d) { return d.size + "px"; })
          .style("font-family", "Impact")
          .style("fill", (d, i) => { return this.fill(i); })
          .attr("text-anchor", "middle")
          .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          })
          .text(function(d) { return d.text; });
      console.log('drawing finished')
    },
    createcloud: function() {
      this.fill = d3.scaleOrdinal(d3.schemeCategory10)
      
      console.log('I am ready to draw')
      var c = cloud().size([1000, 500])
        .words(this.src_Label_Data.map(function(d) {
            return {text: d[0], size: d[1] * 100};
        }))
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 0) * 90; })
        .font("Impact")
        .fontSize(function(d) { return d.size; })
        .on("end", this.draw)
      return c
    },
    compareWordList: function(a,b) {
      if (a.length != b.length) {
        return false
      }
      for (let i = 0; i < a.length; i++){
        if (a[i][0] != b[i][0] || a[i][1] != b[i][1]){
          return false
        }
      }
      return true
    }
  },
  mounted() {
    this.c = this.createcloud()
    this.c.start()
    setInterval(() => {
      axios.get('http://localhost:5001/refreshData').then(
      res => {
            this.src_Labels = res.data.sLabel;
            this.src_Data = res.data.sData;
            var sum = this.findsum(this.src_Data);
            var next_src_Label_Data = []
            for(var i = 0; i < this.src_Labels.length; i++){
                var tmp = [];
                tmp.push(this.src_Labels[i]);
                tmp.push(this.src_Data[i]/sum);
                next_src_Label_Data.push(tmp);
            }
            if (!this.compareWordList(next_src_Label_Data,this.src_Label_Data)) {
              d3.select("svg").remove();
              this.src_Label_Data = next_src_Label_Data
              this.c.words(this.src_Label_Data.map(function(d) {
                    return {text: d[0], size: d[1] * 300};
                })).on("end", this.draw)
              this.c.start()
            }          
          }
      )
    }, 1000);
  },

}
</script>

<style scoped>
#wc{
  overflow: hidden;
  margin: 0 auto;
}

</style>