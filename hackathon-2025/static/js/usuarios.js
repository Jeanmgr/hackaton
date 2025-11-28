let editingId = null;
let users = [];

const tableBody = document.getElementById("usersTableBody");
const roleFilter = document.getElementById("roleFilter");
const modal = document.getElementById("userModal");
const deleteModal = document.getElementById("deleteModal");
const modalTitle = document.getElementById("modalTitle");

// Cargar usuarios desde Firebase (solo roles: admin, intendencia)
async function loadUsers() {
  try {
    const response = await fetch(`/api/usuarios/?t=${Date.now()}`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    users = [];

  const pushUser = (id, userData) => {
      if (!userData || typeof userData !== 'object') return;
      const roleRaw = (userData.Rol || '').toLowerCase();
      const allowed = ['admin', 'intendencia', 'usuario'];
      const role = allowed.includes(roleRaw) ? roleRaw : (roleRaw || 'otro');
      users.push({
          id: id,
          name: `${userData.Nombre || ''} ${userData.Apellidos || ''}`.trim(),
          email: userData.Correo || 'Sin correo',
          role,
          password: userData.Contraseña || ''
        });
      };

    if (Array.isArray(data)) {
      data.forEach((u, idx) => pushUser(String(idx), u));
    } else if (data && typeof data === 'object') {
      Object.entries(data).forEach(([id, u]) => pushUser(id, u));
    }

    renderUsers();
  } catch (err) {
    tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:red;padding:20px;">❌ Error: ${err.message}</td></tr>`;
  }
}

function renderUsers() {
  tableBody.innerHTML = "";
  const f = roleFilter.value;
  const filtered = users.filter(u => f === 'all' || u.role === f);
  if (!filtered.length) {
    tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:var(--text-light)">No hay usuarios para mostrar</td></tr>`;
    return;
  }
  filtered.forEach(u => {
    tableBody.innerHTML += `
      <tr>
        <td>${u.id}</td>
        <td>${u.name}</td>
        <td>${u.email}</td>
        <td><span class="role-badge ${u.role}">${u.role}</span></td>
        <td>
          <button class="action-btn" onclick="openEdit('${u.id}')">✏</button>
          <button class="action-btn" onclick="openDelete('${u.id}')">🗑</button>
        </td>
      </tr>`;
  });
}

roleFilter.addEventListener('change', renderUsers);

document.getElementById('openAddUserBtn').onclick = () => {
  editingId = null;
  modalTitle.textContent = 'Nuevo Usuario';
  document.getElementById('modal_nombre').value = '';
  document.getElementById('modal_apellidos').value = '';
  document.getElementById('modal_email').value = '';
  document.getElementById('modal_password').value = '';
  document.getElementById('modal_role').value = 'admin';
  modal.classList.remove('hidden');
};

document.getElementById('cancelModal').onclick = () => modal.classList.add('hidden');
document.getElementById('cancelDelete').onclick = () => deleteModal.classList.add('hidden');

document.getElementById('saveModal').onclick = async () => {
  const nombre = document.getElementById('modal_nombre').value.trim();
  const apellidos = document.getElementById('modal_apellidos').value.trim();
  const email = document.getElementById('modal_email').value.trim();
  const role = document.getElementById('modal_role').value; // admin | intendencia
  const password = document.getElementById('modal_password').value;

  if (!nombre || !apellidos || !email) return showToast('Completa Nombre, Apellidos y Correo', 'warning');
  if (!editingId && !password) return showToast('La contraseña es obligatoria para nuevos usuarios', 'warning');
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) return showToast('Correo electrónico inválido', 'warning');

  const payload = {
    Nombre: nombre,
    Apellidos: apellidos,
    Correo: email,
    Contraseña: password || 'temporal123',
    Rol: role === 'admin' ? 'Admin' : role === 'intendencia' ? 'Intendencia' : 'Usuario'
  };

  try {
    let userId = editingId;
    let method = 'PUT';
    if (!editingId) {
      // Generar ID simple incremental basado en cantidad actual
      const res = await fetch('/api/usuarios/');
      const cur = await res.json();
      const count = Array.isArray(cur) ? cur.length : Object.keys(cur || {}).length;
      userId = String(count + 1);
      method = 'POST';
    } else if (!password) {
      // Mantener contraseña existente si no se cambia
      const curRes = await fetch(`/api/usuarios/${userId}`);
      const curData = await curRes.json();
      payload.Contraseña = curData.Contraseña || payload.Contraseña;
    }

    const resp = await fetch(`/api/usuarios/${userId}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await resp.json();
    if (!resp.ok) throw new Error(result.detail || 'Error al guardar usuario');

    showToast('Usuario guardado correctamente', 'success');
    modal.classList.add('hidden');
    await loadUsers();
  } catch (err) {
    showToast(String(err.message || err), 'danger');
  }
};

function openEdit(id) {
  editingId = id;
  modalTitle.textContent = 'Editar Usuario';
  const user = users.find(u => u.id === id);
  if (user) {
    const [nombre, ...apArr] = user.name.split(' ');
    document.getElementById('modal_nombre').value = nombre || '';
    document.getElementById('modal_apellidos').value = apArr.join(' ') || '';
    document.getElementById('modal_email').value = user.email || '';
    document.getElementById('modal_role').value = user.role || 'admin';
    document.getElementById('modal_password').value = '';
    document.getElementById('modal_password').placeholder = 'Dejar vacío para mantener contraseña';
  }
  modal.classList.remove('hidden');
}

function openDelete(id) {
  editingId = id;
  const user = users.find(u => u.id === id);
  if (user) {
    document.getElementById('deleteText').textContent = `¿Seguro que deseas eliminar a "${user.name}" (${user.email})?`;
  }
  deleteModal.classList.remove('hidden');
}

document.getElementById('confirmDelete').onclick = async () => {
  try {
    const resp = await fetch(`/api/usuarios/${editingId}`, { method: 'DELETE' });
    const result = await resp.json().catch(() => ({}));
    if (!resp.ok) throw new Error(result.detail || 'Error al eliminar usuario');
    showToast('Usuario eliminado', 'success');
    deleteModal.classList.add('hidden');
    await loadUsers();
  } catch (err) {
    showToast(String(err.message || err), 'danger');
  }
};

// Inicializar
loadUsers();