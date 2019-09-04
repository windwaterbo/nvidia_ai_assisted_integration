import axios from "axios";
const client = axios.create({
  httpsAgent: new https.Agent({
    rejectUnauthorized: false
  }),
  json: true
});

axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
axios.defaults.headers.common['Content-Type'] =
  'application/x-www-form-urlencoded'

// At instance level
// const client = axios.create({
//   httpsAgent: new https.Agent({
//     rejectUnauthorized: false
//   }),
//   json: true
// })
// // At request level
// const agent = new https.Agent({
//   rejectUnauthorized: false
// })








function api(method, resource, data) {
  return client({
      method,
      url: resource,
      headers: [],
      data
    })
    .then(req => {
      return req.data;
    })
    .catch(err => {
      console.log(err)
    });
}
export {
  api
};
