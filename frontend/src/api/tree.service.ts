import httpClient from './httpClient';

export const treeService = {
  async getTree() {
    const { data } = await httpClient.get('/tree/my-tree/');
    if (Array.isArray(data)) return { nodes: data, summary: null };
    return {
      nodes: Array.isArray(data?.nodes) ? data.nodes : [],
      summary: data?.summary ?? null,
    };
  },

  async getGenerations() {
    const { data } = await httpClient.get('/tree/generations-table/');
    return data;
  },

  async recalculate() {
    const { data } = await httpClient.post('/tree/recalculate/');
    return data;
  },
};
