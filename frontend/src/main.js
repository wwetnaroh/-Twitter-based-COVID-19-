import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Element from 'element-plus'
import 'element-plus/dist/index.css'


createApp(App).mount('#app')
const app=createApp(App)
app.use(Element)
app.use(router)
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})
app.mount('#app')