export const apiGet = (path, params) => {
    const endpoint = !params
    ? path
    : `${path}?${
      Object.keys(params)
        .map(k => `${k}=${encodeURIComponent(params[k])}`)
        .join('&')}`;
    return httpRequest('GET', endpoint);
}
export const apiPost = (path, body) => httpRequest('POST', path,  { body: JSON.stringify(body) },{ headers: { 'Content-Type': 'application/json' }} );

async function httpRequest(method, path, options, headers) {
  const url = `https://apps.hdap.gatech.edu/ss2backend/api/v1/${path}`;
  const response = fetch(url, {
    ...options,
    method,
    ...headers
  });

  let data;

  try {
    const res = await response;
    data = res.json();
    return data;
  } catch (err) {
    return err;
  }
}
