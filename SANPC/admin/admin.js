const accessPanel = document.querySelector('#access-panel');
const accessTitle = document.querySelector('#access-title');
const accessCopy = document.querySelector('#access-copy');
const accessMessage = document.querySelector('#access-message');
const loginForm = document.querySelector('#login-form');
const dashboard = document.querySelector('#dashboard');
const productForm = document.querySelector('#product-form');
const productMessage = document.querySelector('#product-message');
const inventoryList = document.querySelector('#inventory-list');
const inventoryEmpty = document.querySelector('#inventory-empty');
const productCount = document.querySelector('#product-count');
const toast = document.querySelector('#admin-toast');
const inventorySearch = document.querySelector('#inventory-search');
const inventoryCategory = document.querySelector('#inventory-category');
const imageInput = document.querySelector('#product-image');
const imagePreview = document.querySelector('#image-preview');
let toastTimer;
let inventoryProducts = [];
let previewUrl = '';

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function setMessage(element, message, isError = true) {
  element.textContent = message;
  element.classList.toggle('is-error', isError && Boolean(message));
  element.classList.toggle('is-success', !isError && Boolean(message));
}

async function request(url, options = {}) {
  const response = await fetch(url, { credentials: 'same-origin', ...options });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || 'Có lỗi xảy ra. Vui lòng thử lại.');
  return payload;
}

function showDashboard() {
  accessPanel.hidden = true;
  dashboard.hidden = false;
  loadInventory();
}

function showAccess(configured) {
  dashboard.hidden = true;
  accessPanel.hidden = false;
  accessTitle.textContent = 'Đăng nhập SANPC';
  accessCopy.textContent = 'Chỉ chủ cửa hàng có mật khẩu mới được quản lý sản phẩm.';
  loginForm.hidden = false;
  if (!configured) setMessage(accessMessage, 'Tài khoản chủ chưa được thiết lập trên máy chủ.');
}

async function checkSession() {
  try {
    const status = await request('/api/admin/status');
    if (status.authenticated) showDashboard();
    else showAccess(status.configured);
  } catch (error) {
    showAccess(true);
    setMessage(accessMessage, `${error.message} Hãy chạy máy chủ SANPC rồi tải lại trang.`);
  }
}

loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const password = String(new FormData(loginForm).get('password'));
  try {
    await request('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password })
    });
    loginForm.reset();
    setMessage(accessMessage, 'Đăng nhập thành công.', false);
    showDashboard();
  } catch (error) {
    setMessage(accessMessage, error.message);
  }
});

async function loadInventory() {
  inventoryList.innerHTML = '<p class="inventory-loading">Đang tải sản phẩm…</p>';
  try {
    inventoryProducts = await request('/api/products');
    renderInventory();
  } catch (error) {
    inventoryList.innerHTML = '';
    setMessage(productMessage, error.message);
  }
}

function renderInventory() {
  const query = inventorySearch.value.trim().toLocaleLowerCase('vi');
  const category = inventoryCategory.value;
  const filtered = inventoryProducts.filter((item) => {
    const content = `${item.title} ${item.category} ${item.location}`.toLocaleLowerCase('vi');
    return content.includes(query) && (category === 'all' || item.category === category);
  });
  productCount.textContent = inventoryProducts.length;
  inventoryEmpty.hidden = inventoryProducts.length > 0;
  document.querySelector('#inventory-no-match').hidden = inventoryProducts.length === 0 || filtered.length > 0;
  inventoryList.innerHTML = filtered.map((item) => `
      <article class="inventory-item">
        <img src="${escapeHtml(item.image)}" alt="" loading="lazy" onerror="this.style.visibility='hidden'">
        <div class="inventory-info"><span>${escapeHtml(item.category)} · ${escapeHtml(item.condition)}</span><h3>${escapeHtml(item.title)}</h3><strong>${new Intl.NumberFormat('vi-VN').format(item.price)} ₫</strong><small>⌖ ${escapeHtml(item.location)}</small></div>
        <button class="delete-product" type="button" data-delete="${escapeHtml(item.id)}" aria-label="Xóa ${escapeHtml(item.title)}" title="Xóa sản phẩm">×</button>
      </article>`).join('');
}

productForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  setMessage(productMessage, '');
  const submitButton = productForm.querySelector('[type="submit"]');
  submitButton.disabled = true;
  submitButton.textContent = 'Đang đăng…';
  try {
    await request('/api/admin/products', { method: 'POST', body: new FormData(productForm) });
    productForm.reset();
    setMessage(productMessage, 'Sản phẩm đã xuất hiện trên website khách.', false);
    await loadInventory();
  } catch (error) {
    setMessage(productMessage, error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Đăng sản phẩm lên website ↗';
  }
});

inventoryList.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-delete]');
  if (!button || !window.confirm('Gỡ sản phẩm này khỏi website khách?')) return;
  button.disabled = true;
  try {
    await request(`/api/admin/products/${encodeURIComponent(button.dataset.delete)}`, { method: 'DELETE' });
    await loadInventory();
    toast.textContent = 'Đã gỡ sản phẩm khỏi website.';
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2400);
  } catch (error) {
    button.disabled = false;
    setMessage(productMessage, error.message);
  }
});

document.querySelector('#logout-button').addEventListener('click', async () => {
  try {
    await request('/api/admin/logout', { method: 'POST' });
  } finally {
    showAccess(true);
    setMessage(accessMessage, 'Bạn đã đăng xuất.', false);
  }
});

document.querySelector('#refresh-button').addEventListener('click', loadInventory);
inventorySearch.addEventListener('input', renderInventory);
inventoryCategory.addEventListener('change', renderInventory);
imageInput.addEventListener('change', () => {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  const imageFile = imageInput.files?.[0];
  if (!imageFile) {
    imagePreview.hidden = true;
    imagePreview.removeAttribute('src');
    previewUrl = '';
    return;
  }
  previewUrl = URL.createObjectURL(imageFile);
  imagePreview.src = previewUrl;
  imagePreview.hidden = false;
});
checkSession();
