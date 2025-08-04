// https://nuxt.com/docs/api/configuration/nuxt-config
import axios from 'axios'


export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  target: 'static',
  ssr: false,
  modules: [
    '@nuxt/content',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/fonts'
  ],
  routeRules: {
    '/room/**': { static: true },
  },
  nitro: {
    prerender: {
      // Exclude specific routes from prerendering
      // For example, if you have a dynamic route like /products/[id]
      // and you want it to always be SSR.
      routes: ['/'], // Only prerender the homepage, for example
      // Or if you want to explicitly exclude certain patterns:
      // ignore: ['/products/**'],
    },
  },
  hooks: {
    async 'prerender:routes'(ctx) {
      const URL_MENU_BASE = 'http://192.168.108.18:3002/api'
      const resp = await axios.get(`${URL_MENU_BASE}/menu/all`)
      console.log(resp.data)
      const rooms = resp.data.rooms.map(room => `/room/${room.id}`);

      // Add them to the routes to be prerendered
      rooms.forEach(route => ctx.routes.add(route));

      // You can also add other static routes or API routes here
      // ctx.routes.add('/about-us');
      // Example: Prerendering an API route that will be served statically
      // ctx.routes.add('/api/blog-posts.json');
    },
  }
})