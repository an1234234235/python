const fallbackImages = {
  GPU: 'https://images.unsplash.com/photo-1591488320449-011701bb6704?auto=format&fit=crop&w=900&q=82',
  CPU: 'https://images.unsplash.com/photo-1555617981-dac3880eac6e?auto=format&fit=crop&w=900&q=82',
  RAM: 'https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=900&q=82',
  'PC bộ': 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=900&q=82',
  'Màn hình': 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=82',
  Mainboard: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=82'
};

const loadStored = (key, fallback) => {
  try {
    const value = JSON.parse(localStorage.getItem(key));
    return value ?? fallback;
  } catch {
    return fallback;
  }
};

let listings = [];
let listingsLoadFailed = false;
let favorites = new Set(loadStored('chopc-favorites', []));
let activeCategory = 'all';
let favoritesOnly = false;
let toastTimer;

const grid = document.querySelector('#listing-grid');
const count = document.querySelector('#listing-count');
const emptyState = document.querySelector('#empty-state');
const searchInput = document.querySelector('#search-input');
const locationFilter = document.querySelector('#location-filter');
const sortSelect = document.querySelector('#sort-select');
const favoritesToggle = document.querySelector('#favorites-toggle');
const favoriteCount = document.querySelector('#favorite-count');
const detailDialog = document.querySelector('#detail-dialog');
const toast = document.querySelector('#toast');

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[character]);
}

function formatPrice(price) {
  return `${new Intl.NumberFormat('vi-VN').format(price)} ₫`;
}

function persist() {
  try {
    localStorage.setItem('chopc-favorites', JSON.stringify([...favorites]));
  } catch {
    showToast('Không thể lưu dữ liệu trên thiết bị này.');
  }
}

function visibleListings() {
  const term = searchInput.value.trim().toLocaleLowerCase('vi');
  const selectedLocation = locationFilter.value;
  const result = listings.filter((item) => {
    const matchesCategory = activeCategory === 'all' || item.category === activeCategory;
    const matchesLocation = selectedLocation === 'all' || item.location === selectedLocation;
    const matchesFavorite = !favoritesOnly || favorites.has(item.id);
    const searchable = `${item.title} ${item.category} ${item.location} ${item.seller} ${item.description}`.toLocaleLowerCase('vi');
    return matchesCategory && matchesLocation && matchesFavorite && searchable.includes(term);
  });
  if (sortSelect.value === 'price-low') result.sort((a, b) => a.price - b.price);
  if (sortSelect.value === 'price-high') result.sort((a, b) => b.price - a.price);
  if (sortSelect.value === 'newest') result.sort((a, b) => listings.indexOf(a) - listings.indexOf(b));
  return result;
}

function render() {
  const visible = visibleListings();
  count.textContent = visible.length;
  favoriteCount.textContent = favorites.size;
  favoritesToggle.classList.toggle('is-active', favoritesOnly);
  favoritesToggle.setAttribute('aria-pressed', String(favoritesOnly));
  emptyState.hidden = visible.length > 0;
  if (visible.length === 0) {
    const emptyTitle = emptyState.querySelector('h3');
    const emptyCopy = emptyState.querySelector('p');
    const clearFilters = emptyState.querySelector('#clear-filters');
    const hasFilters = searchInput.value.trim() || activeCategory !== 'all' || locationFilter.value !== 'all' || favoritesOnly;
    if (listingsLoadFailed) {
      emptyTitle.textContent = 'Chưa kết nối được SANPC';
      emptyCopy.textContent = 'Vui lòng tải website từ máy chủ SANPC rồi thử lại.';
      clearFilters.hidden = true;
    } else if (listings.length === 0) {
      emptyTitle.textContent = 'SANPC đang cập nhật sản phẩm';
      emptyCopy.textContent = 'Sản phẩm mới sẽ được đăng tại đây.';
      clearFilters.hidden = true;
    } else {
      emptyTitle.textContent = 'Chưa thấy món này';
      emptyCopy.textContent = 'Thử từ khóa khác hoặc bỏ bớt bộ lọc nhé.';
      clearFilters.hidden = !hasFilters;
    }
  }
  grid.innerHTML = visible.map((item, index) => `
    <article class="listing-card" style="animation-delay:${Math.min(index * 45, 240)}ms">
      <div class="card-photo" data-detail="${escapeHtml(item.id)}" tabindex="0" role="button" aria-label="Xem ${escapeHtml(item.title)}">
        <img src="${escapeHtml(item.image || fallbackImages[item.category] || fallbackImages.GPU)}" alt="${escapeHtml(item.title)}" loading="lazy" onerror="this.onerror=null;this.src='${fallbackImages[item.category] || fallbackImages.GPU}'">
        <span class="condition-tag">${escapeHtml(item.condition)}</span>
        <button class="heart-button${favorites.has(item.id) ? ' is-favorite' : ''}" type="button" data-favorite="${escapeHtml(item.id)}" aria-label="${favorites.has(item.id) ? 'Bỏ lưu tin' : 'Lưu tin'}" aria-pressed="${favorites.has(item.id)}">${favorites.has(item.id) ? '♥' : '♡'}</button>
      </div>
      <div class="card-body">
        <div class="card-meta"><span class="card-category">${escapeHtml(item.category)}</span><span>${escapeHtml(item.age || 'Vừa đăng')}</span></div>
        <button class="card-title" type="button" data-detail="${escapeHtml(item.id)}">${escapeHtml(item.title)}</button>
        <p class="card-description">${escapeHtml(item.description || 'Người bán chưa thêm mô tả.')}</p>
        <div class="card-bottom">
          <div><div class="card-price">${formatPrice(item.price)}</div><div class="card-location">⌖ ${escapeHtml(item.location)}</div></div>
          <span class="seller-mark" title="SANPC">SANPC</span>
        </div>
        <div class="card-actions"><a class="card-contact-zalo" href="https://zalo.me/0948078595" target="_blank" rel="noopener noreferrer">Zalo</a><a class="card-contact-phone" href="tel:+84948078595">Gọi tư vấn</a></div>
      </div>
    </article>`).join('');
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('is-visible');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2400);
}

function openDetails(id) {
  const item = listings.find((listing) => listing.id === id);
  if (!item) return;
  const image = item.image || fallbackImages[item.category] || fallbackImages.GPU;
  document.querySelector('#detail-content').innerHTML = `
    <img class="detail-photo" src="${escapeHtml(image)}" alt="${escapeHtml(item.title)}" onerror="this.onerror=null;this.src='${fallbackImages[item.category] || fallbackImages.GPU}'">
    <div class="detail-body">
      <div class="card-meta"><span class="card-category">${escapeHtml(item.category)} · ${escapeHtml(item.condition)}</span><span>${escapeHtml(item.age || 'Vừa đăng')}</span></div>
      <h2 id="detail-title">${escapeHtml(item.title)}</h2>
      <div class="detail-price">${formatPrice(item.price)}</div>
      <p class="detail-desc">${escapeHtml(item.description || 'Người bán chưa thêm mô tả.')}</p>
      <div class="detail-contact"><p><strong>SANPC tư vấn</strong><small>⌖ ${escapeHtml(item.location)} · 0948 078 595</small></p><div class="contact-actions"><a class="button button-zalo" href="https://zalo.me/0948078595" target="_blank" rel="noopener noreferrer">Nhắn Zalo ↗</a><a class="button button-dark" href="tel:+84948078595">Gọi SANPC ↗</a></div></div>
    </div>`;
  detailDialog.showModal();
}

async function loadListings() {
  try {
    const response = await fetch('/api/products', { cache: 'no-store' });
    if (!response.ok) throw new Error('Không thể tải sản phẩm từ SANPC.');
    listings = await response.json();
    if (!Array.isArray(listings)) throw new Error('Dữ liệu sản phẩm không hợp lệ.');
    listingsLoadFailed = false;
    render();
  } catch {
    listings = [];
    listingsLoadFailed = true;
    render();
    showToast('Không kết nối được máy chủ SANPC. Hãy tải trang từ địa chỉ website.');
  }
}

document.querySelector('#search-form').addEventListener('submit', (event) => {
  event.preventDefault();
  render();
});
searchInput.addEventListener('input', render);
locationFilter.addEventListener('change', render);
sortSelect.addEventListener('change', render);

document.querySelector('.category-strip').addEventListener('click', (event) => {
  const chip = event.target.closest('[data-category]');
  if (!chip) return;
  activeCategory = chip.dataset.category;
  document.querySelectorAll('.category-chip').forEach((button) => button.classList.toggle('is-selected', button === chip));
  favoritesOnly = false;
  render();
});

favoritesToggle.addEventListener('click', () => {
  favoritesOnly = !favoritesOnly;
  render();
});

grid.addEventListener('click', (event) => {
  const favoriteButton = event.target.closest('[data-favorite]');
  if (favoriteButton) {
    const id = favoriteButton.dataset.favorite;
    if (favorites.has(id)) favorites.delete(id);
    else favorites.add(id);
    persist();
    render();
    return;
  }
  const detailButton = event.target.closest('[data-detail]');
  if (detailButton) openDetails(detailButton.dataset.detail);
});

grid.addEventListener('keydown', (event) => {
  if ((event.key === 'Enter' || event.key === ' ') && event.target.matches('[data-detail][role="button"]')) {
    event.preventDefault();
    openDetails(event.target.dataset.detail);
  }
});

document.querySelector('.detail-close').addEventListener('click', () => detailDialog.close());
document.querySelector('#clear-filters').addEventListener('click', () => {
  activeCategory = 'all';
  favoritesOnly = false;
  searchInput.value = '';
  locationFilter.value = 'all';
  sortSelect.value = 'newest';
  document.querySelectorAll('.category-chip').forEach((chip) => chip.classList.toggle('is-selected', chip.dataset.category === 'all'));
  render();
});

loadListings();