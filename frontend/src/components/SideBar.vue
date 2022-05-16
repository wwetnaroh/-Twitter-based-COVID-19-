<template>
  <div id="sidebar">
      <div id="navilist">   
        <a class="navibutton" :class="$route.path =='/map'?'active':''" href="/map"><div class="navicontent">Covid-19 US Map</div></a>
        <a class="navibutton" :class="$route.path =='/twitter'?'active':''" href="/twitter"><div class="navicontent">Covid-19 Twitter Hot Topics</div></a>
      </div>
  </div>
</template>

<script>
export default {
  name: 'SideBar',
  data() {
   return{}
  }
}
</script>

<style scoped>
#sidebar {
 /* position: absolute; */
 float: left;
 width: 10%;
 height: 100%;
 background-color: rgb(75, 75, 75);
}
#navilist {
 margin: 20% 0;
}
.navibutton {
 display: flex;
 align-items: center;
 /* justify-content: center; */
 height: 10vh;
 color: white;
 text-decoration: none;
 margin: 20px 0;
 transition: background-color 0.5s ease-out;
}
.navibutton:hover { 
 background-color: rgb(128, 67, 67);
}
.navicontent {
 display: inline-block;
 margin: 0 10px;
}
.active {
 background-color: rgb(128, 67, 67);
 border-left: 5px solid red;
}
</style>
