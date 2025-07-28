// src/api.js
import axios from 'axios';

// Replace these with actual values
// const API_KEY = '428fdd4daeb7690';
// const API_SECRET = 'd041aa9e9c96a7e';

// const api = axios.create({
//   baseURL: 'http://pspl.com:8000/api/resource',// Change if Frappe is on a different URL or port
//   headers: {
//     Authorization: `token ${API_KEY}:${API_SECRET}`
//   },
//   withCredentials: true,// Required for cookie-based auth
// });

// const frappe = axios.create({
//   baseURL: 'http://pspl.com:8000/api/method',
//   headers: {
//     Authorization: `token ${API_KEY}:${API_SECRET}`
//   },
//   withCredentials: true,
// })

// export { api, frappe };
const baseURL = 'http://pspl.com:8000'; // Update if needed

const api = axios.create({
  baseURL: `${baseURL}/api/resource`,
  withCredentials: true, // Required for session cookies (sid)
});

const frappe = axios.create({
  baseURL: `${baseURL}/api/method`,
  withCredentials: true,
});

export { api, frappe, baseURL };
