/**
 * Renderer Registry
 * Manages registration and dispatching of content and interaction renderers.
 */

window.RendererRegistry = {
  renderers: {},
  register(contentForm, interactionMode, fn) {
    const key = `${contentForm}:${interactionMode}`;
    this.renderers[key] = fn;
  },
  registerContent(contentForm, fn) {
    this.renderers[contentForm] = fn;
  },
  registerInteraction(mode, fn) {
    this.renderers[mode] = fn;
  },
  dispatch(node) {
    const contentForm = node.content_form || 'unknown';
    const outputMode = node.output_mode || 'none';
    const key = `${contentForm}:${outputMode}`;

    let contentHtml = '';
    let interactionHtml = '';

    if (this.renderers[key]) {
      contentHtml = this.renderers[key](node) || '';
    } else if (this.renderers[contentForm]) {
      contentHtml = this.renderers[contentForm](node) || '';
    } else {
      contentHtml = this.renderFallback(node);
    }

    // Interaction dispatch (if separate)
    if (this.renderers[outputMode]) {
      interactionHtml = this.renderers[outputMode](node) || '';
    }

    return { contentHtml, interactionHtml };
  },
  renderFallback(node) {
    if (window.renderDataInspection) {
      const payload = node.payload || {};
      const reason = `未知的內容類型: ${node.content_form}`;
      return window.renderDataInspection(payload, reason);
    }
    return `<div>Error: Unknown content form ${node.content_form} and no fallback renderer found.</div>`;
  }
};
