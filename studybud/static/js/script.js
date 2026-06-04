// Dropdown Menu
const dropdown = document.getElementById("userDropdown");
const dropdownToggle = document.getElementById("userDropdownToggle");

if (dropdownToggle && dropdown) {
  dropdownToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("show");
  });

  document.addEventListener("click", () => {
    dropdown.classList.remove("show");
  });

  dropdown.addEventListener("click", (e) => {
    e.stopPropagation();
  });
}

// Avatar upload preview
const avatarInput = document.querySelector("#id_avatar");
const avatarPreview = document.querySelector("#avatarPreview");

if (avatarInput && avatarPreview) {
  avatarInput.addEventListener("change", () => {
    const [file] = avatarInput.files;
    if (file) {
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.alt = "Avatar preview";
      avatarPreview.innerHTML = "";
      avatarPreview.appendChild(img);
    }
  });
}

// Scroll to Bottom
const chatBody = document.getElementById("chatBody");
if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;

// Toast Notification System
function showToast(message, type = "info", duration = 4000) {
  let container = document.querySelector(".toast-container");

  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.innerHTML = `
    <div class="toast__message">${message}</div>
  `;

  toast.addEventListener("click", () => {
    toast.classList.add("toast--exiting");
    setTimeout(() => toast.remove(), 200);
  });

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.isConnected) {
      toast.classList.add("toast--exiting");
      setTimeout(() => toast.remove(), 200);
    }
  }, duration);
}

// Convert Django message framework toasts
const djangoMessages = document.querySelectorAll(".toast");
djangoMessages.forEach((el) => {
  const message = el.querySelector(".toast__message")?.textContent;
  if (message) {
    const type = Array.from(el.classList).find((c) => c.startsWith("toast--"))?.replace("toast--", "") || "info";
    setTimeout(() => {
      el.classList.add("toast--exiting");
      setTimeout(() => el.remove(), 200);
    }, 4000);
  }
});



// Scroll-to-bottom button
const scrollBtn = document.getElementById("scrollToBottom");
const chatBodyEl = document.getElementById("chatBody");

if (scrollBtn && chatBodyEl) {
  chatBodyEl.addEventListener("scroll", () => {
    const threshold = 200;
    const isNearBottom =
      chatBodyEl.scrollHeight - chatBodyEl.scrollTop - chatBodyEl.clientHeight < threshold;

    if (!isNearBottom) {
      scrollBtn.classList.add("chat__scroll-bottom--visible");
    } else {
      scrollBtn.classList.remove("chat__scroll-bottom--visible");
    }
  });

  scrollBtn.addEventListener("click", () => {
    chatBodyEl.scrollTo({ top: chatBodyEl.scrollHeight, behavior: "smooth" });
  });
}

// Form submission loading states
document.querySelectorAll("form").forEach((form) => {
  const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
  if (!submitBtn) return;

  form.addEventListener("submit", () => {
    submitBtn.disabled = true;
    submitBtn.classList.add("btn--loading");
    const text = submitBtn.querySelector(".btn__text");
    const spinner = submitBtn.querySelector(".btn__spinner");
    if (text) text.style.display = "none";
    if (spinner) spinner.style.display = "inline-flex";
  });
});

// Password show/hide toggle
document.querySelectorAll(".password-toggle").forEach((toggle) => {
  toggle.addEventListener("click", () => {
    const input = toggle.closest(".password-wrapper").querySelector("input");
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";

    const [eyeOpen, eyeClosed] = toggle.querySelectorAll("svg");
    if (eyeOpen && eyeClosed) {
      eyeOpen.style.display = isPassword ? "none" : "block";
      eyeClosed.style.display = isPassword ? "block" : "none";
    }
  });
});

// Password strength indicator
const passwordInput = document.querySelector("#id_password1");
const strengthBar = document.getElementById("password-strength-bar");

if (passwordInput && strengthBar) {
  passwordInput.addEventListener("input", () => {
    const val = passwordInput.value;
    let score = 0;

    if (val.length >= 8) score++;
    if (val.match(/[a-z]/) && val.match(/[A-Z]/)) score++;
    if (val.match(/\d/)) score++;
    if (val.match(/[^a-zA-Z\d]/)) score++;

    let strength = "weak";
    if (score >= 3) strength = "strong";
    else if (score >= 2) strength = "medium";

    const fill = strengthBar.querySelector(".password-strength__fill");
    const text = passwordInput
      .closest(".form__group")
      ?.querySelector(".password-strength__text");

    if (fill) {
      fill.className = `password-strength__fill password-strength__fill--${strength}`;
    }

    if (text) {
      const labels = {
        weak: "Weak - try adding more variety",
        medium: "Medium - getting better",
        strong: "Strong password",
      };
      text.textContent = labels[strength];
    }
  });
}

// Mobile search toggle
const mobileSearchToggle = document.querySelector(".mobile-search-toggle");
const headerSearch = document.querySelector(".header__search");

if (mobileSearchToggle && headerSearch) {
  mobileSearchToggle.addEventListener("click", () => {
    const mobileSearch = headerSearch.cloneNode(true);
    mobileSearch.classList.add("header__search--mobile");

    const existing = document.querySelector(".header__search--mobile");
    if (existing) {
      existing.remove();
      return;
    }

    headerSearch.parentElement.insertAdjacentElement("afterend", mobileSearch);

    const input = mobileSearch.querySelector("input");
    if (input) input.focus();
  });
}

// Character counter on textarea
document.querySelectorAll("textarea[maxlength]").forEach((textarea) => {
  const container = textarea.closest(".form__group");
  if (!container) return;

  const countEl = document.createElement("div");
  countEl.className = "char-count";

  const max = parseInt(textarea.getAttribute("maxlength"), 10);

  const update = () => {
    const len = textarea.value.length;
    countEl.textContent = `${len}/${max}`;
    countEl.className = "char-count";
    if (len > max * 0.9) countEl.classList.add("char-count--warn");
    if (len >= max) countEl.classList.add("char-count--error");
  };

  textarea.addEventListener("input", update);
  container.appendChild(countEl);
  update();
});

// Press-down effect on cards and sidebar items
document.querySelectorAll('.room-card, .sidebar-item, .topics__link').forEach(item => {
  item.addEventListener('mousedown', () => {
    item.classList.add('scale-[0.98]');
  });
  item.addEventListener('mouseup', () => {
    item.classList.remove('scale-[0.98]');
  });
  item.addEventListener('mouseleave', () => {
    item.classList.remove('scale-[0.98]');
  });
});

// IntersectionObserver for stagger animations
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.visibility = 'visible';
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.1 });

document.querySelectorAll('.animate-fadeInUp').forEach(el => {
  observer.observe(el);
});

// Toast close buttons
document.querySelectorAll('.toast__close').forEach(btn => {
  btn.addEventListener('click', () => {
    const toast = btn.closest('.toast');
    toast.classList.add('toast--exiting');
    setTimeout(() => toast.remove(), 200);
  });
});

// Topic chip selection
document.querySelectorAll(".topic-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    const input = document.querySelector("input[name='topic']");
    if (input) {
      input.value = chip.textContent.trim();
    }
    document
      .querySelectorAll(".topic-chip")
      .forEach((c) => c.classList.remove("topic-chip--active"));
    chip.classList.add("topic-chip--active");
  });
});
