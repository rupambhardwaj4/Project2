// QT Consultancy HR & Payroll Systems - Shared Core Controller

// Default Corporate Employee Seed Database
const DEFAULT_EMPLOYEES = [];

// Initialize State
let state = {
    employees: [],
    auditLogs: [],
    payrollRuns: [],
    currentUser: null,
    currentPeriod: "June 2026",
    selectedEmployee: null
};

// State Synchronization & Central Branding Schema
const DEFAULT_COMPANY_SETTINGS = {
    shortName: "QT Consultancy",
    fullLegalName: "QT Consultancy Private Limited",
    headOfficeAddress: "12th Floor, DLF Cyber City, Sector 21\nGurgaon, Haryana - 122002",
    supportEmail: "hr@qtconsultancy.in",
    contactPhone: "+91 9899844927",
    logoInitials: "QT",
    logoImage: null,
    signatureImage: null,
    sealImage: null,
    primaryColor: "#88BDF2",
    sidebarColor: "#384959",
    gstin: "09AABCQ0892L1Z0",
    stateCode: "09",
    websiteUrl: "https://qtconsultancy.in",
    applySignatureToInvoice: true,
    applySignatureToSalarySlip: true,
    applySealToInvoice: true,
    applySealToSalarySlip: true
};

function saveStateToStorage() {
    localStorage.setItem("qt_consultancy_state", JSON.stringify(state));
}

function upgradeStateSettings() {
    if (!state.companySettings) {
        state.companySettings = {};
    }
    
    // Migrate legacy settings if they exist
    const legacy = state.settings || {};
    
    state.companySettings.shortName = state.companySettings.shortName || legacy.companyName || DEFAULT_COMPANY_SETTINGS.shortName;
    state.companySettings.fullLegalName = state.companySettings.fullLegalName || legacy.companyNameFull || DEFAULT_COMPANY_SETTINGS.fullLegalName;
    state.companySettings.headOfficeAddress = state.companySettings.headOfficeAddress || legacy.address || DEFAULT_COMPANY_SETTINGS.headOfficeAddress;
    state.companySettings.supportEmail = state.companySettings.supportEmail || legacy.email || DEFAULT_COMPANY_SETTINGS.supportEmail;
    state.companySettings.contactPhone = state.companySettings.contactPhone || legacy.phone || DEFAULT_COMPANY_SETTINGS.contactPhone;
    state.companySettings.logoInitials = state.companySettings.logoInitials || legacy.logoText || DEFAULT_COMPANY_SETTINGS.logoInitials;
    
    state.companySettings.logoImage = state.companySettings.logoImage !== undefined ? state.companySettings.logoImage : (legacy.logoImage || DEFAULT_COMPANY_SETTINGS.logoImage);
    state.companySettings.signatureImage = state.companySettings.signatureImage !== undefined ? state.companySettings.signatureImage : (legacy.signatureImage || DEFAULT_COMPANY_SETTINGS.signatureImage);
    state.companySettings.sealImage = state.companySettings.sealImage !== undefined ? state.companySettings.sealImage : (legacy.stampImage || DEFAULT_COMPANY_SETTINGS.sealImage);
    
    state.companySettings.primaryColor = state.companySettings.primaryColor || legacy.themeColor || DEFAULT_COMPANY_SETTINGS.primaryColor;
    state.companySettings.sidebarColor = state.companySettings.sidebarColor || legacy.themeColorDark || DEFAULT_COMPANY_SETTINGS.sidebarColor;
    
    state.companySettings.gstin = state.companySettings.gstin || DEFAULT_COMPANY_SETTINGS.gstin;
    state.companySettings.stateCode = state.companySettings.stateCode || DEFAULT_COMPANY_SETTINGS.stateCode;
    state.companySettings.websiteUrl = state.companySettings.websiteUrl || DEFAULT_COMPANY_SETTINGS.websiteUrl;

    state.companySettings.applySignatureToInvoice = state.companySettings.applySignatureToInvoice !== undefined ? state.companySettings.applySignatureToInvoice : DEFAULT_COMPANY_SETTINGS.applySignatureToInvoice;
    state.companySettings.applySignatureToSalarySlip = state.companySettings.applySignatureToSalarySlip !== undefined ? state.companySettings.applySignatureToSalarySlip : DEFAULT_COMPANY_SETTINGS.applySignatureToSalarySlip;
    state.companySettings.applySealToInvoice = state.companySettings.applySealToInvoice !== undefined ? state.companySettings.applySealToInvoice : DEFAULT_COMPANY_SETTINGS.applySealToInvoice;
    state.companySettings.applySealToSalarySlip = state.companySettings.applySealToSalarySlip !== undefined ? state.companySettings.applySealToSalarySlip : DEFAULT_COMPANY_SETTINGS.applySealToSalarySlip;
    
    // Clean up legacy settings key to avoid confusion, but provide a safe getter on state
    delete state.settings;
}

// Add a getter/setter to state for compatibility with any residual page scripts reading state.settings
if (typeof state !== 'undefined') {
    Object.defineProperty(state, 'settings', {
        get: function() { return state.companySettings; },
        set: function(val) { state.companySettings = val; },
        configurable: true
    });
}

function loadStateFromStorage() {
    const cached = localStorage.getItem("qt_consultancy_state");
    if (cached) {
        try {
            state = JSON.parse(cached);
            upgradeStateSettings();
        } catch (e) {
            console.error("Error loading cached state, resetting", e);
            resetStateToDefault();
        }
    } else {
        resetStateToDefault();
    }
}

function resetStateToDefault() {
    state.employees = JSON.parse(JSON.stringify(DEFAULT_EMPLOYEES));
    state.companySettings = JSON.parse(JSON.stringify(DEFAULT_COMPANY_SETTINGS));
    state.auditLogs = [
        { timestamp: new Date(Date.now() - 3600000 * 24).toISOString(), message: "Corporate registry database initialized." },
        { timestamp: new Date(Date.now() - 3600000 * 4).toISOString(), message: "Tax parameters and compliance coefficients updated." }
    ];
    state.payrollRuns = [];
    state.currentUser = state.currentUser || null; // preserve login session if reset
    state.currentPeriod = "June 2026";
    state.selectedEmployee = null;
    saveStateToStorage();
}

function loadCompanySettings() {
    loadStateFromStorage();
}

// -------------------------------------------------------------
// TOAST NOTIFICATIONS
// -------------------------------------------------------------
const Toast = {
    show(message, type = "success") {
        const container = document.getElementById("toast-container");
        if (!container) return;

        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        
        let icon = "🔔";
        if (type === "success") icon = "✅";
        if (type === "warning") icon = "⚠️";
        if (type === "danger") icon = "❌";
        if (type === "info") icon = "ℹ️";

        toast.innerHTML = `
            <span style="font-size: 1.1rem;">${icon}</span>
            <div class="toast-message">${message}</div>
        `;
        container.appendChild(toast);

        // Auto remove
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(50px)";
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
};

// -------------------------------------------------------------
// AUDIT LOG SYSTEM
// -------------------------------------------------------------
const Auditor = {
    log(message) {
        const newLog = {
            timestamp: new Date().toISOString(),
            message: message
        };
        state.auditLogs.unshift(newLog); // Newest first
        saveStateToStorage();
        
        const container = document.getElementById("audit-log-list");
        if (container) this.render();
    },
    
    render() {
        const container = document.getElementById("audit-log-list");
        if (!container) return;
        
        if (state.auditLogs.length === 0) {
            container.innerHTML = `<div style="text-align: center; color: var(--text-muted); font-size: 0.875rem; padding: 20px;">No administrative operations logged.</div>`;
            return;
        }

        container.innerHTML = state.auditLogs.map(log => {
            const date = new Date(log.timestamp);
            const timeStr = date.toLocaleDateString() + " " + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            return `
                <div class="audit-item">
                    <span class="audit-time">${timeStr}</span>
                    <span class="audit-desc">${log.message}</span>
                </div>
            `;
        }).join("");
    }
};

// -------------------------------------------------------------
// FINANCIAL CALCULATOR UTILITY
// -------------------------------------------------------------
const FinanceCalculator = {
    calculate(emp) {
        if (emp.isVendorStaff) {
            const workingDays = parseFloat(emp.workingDays) || 0;
            const perDayPayment = parseFloat(emp.perDayPayment) || 0;
            const incentive = parseFloat(emp.incentive) || 0;
            const serviceCharge = parseFloat(emp.serviceCharge) || 0;

            const candidatePayout = workingDays * perDayPayment + incentive;
            const tds = candidatePayout * 0.01;
            const net = candidatePayout - tds;
            const vendorPayout = candidatePayout + serviceCharge;
            const gst = vendorPayout * 0.18;
            const totalPayment = vendorPayout + gst;

            return {
                basePay: emp.baseSalary, // Total Salary
                overtimePay: incentive, // map incentive
                grossPay: candidatePayout,
                taxAmount: tds,
                netPay: totalPayment, // Net Pay shows Total Payment
                
                isVendorStaff: true,
                workingDays,
                perDayPayment,
                incentive,
                tds,
                net,
                serviceCharge,
                vendorPayout,
                gst,
                totalPayment
            };
        }

        let basePay = emp.baseSalary;
        let overtimePay = 0;
        let rate = emp.hourlyRate;

        // Overtime check: active and hours worked exceed 160 hours
        if (emp.status === "Active" && emp.timesheetStatus === "Uploaded" && emp.hoursWorked > 160) {
            const overtimeHours = emp.hoursWorked - 160;
            overtimePay = overtimeHours * (rate * 1.5);
        }

        let grossPay = 0;
        let taxAmount = 0;
        let netPay = 0;

        if (emp.status === "Active") {
            grossPay = basePay + overtimePay + emp.allowance;
            taxAmount = grossPay * 0.15; // 15% flat tax bracket
            netPay = grossPay - taxAmount - emp.deductions;
        }

        return {
            basePay,
            overtimePay,
            grossPay,
            taxAmount,
            netPay
        };
    }
};

// -------------------------------------------------------------
// SESSION SECURITY & BOOTSTRAP INITIALIZER
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // 1. Sync local data
    loadStateFromStorage();
    
    // Apply branding settings
    loadCompanySettings();
    applyCompanyBranding();

    // Clean up old default seed employees if present
    const defaultIds = ["QT-001", "QT-002", "QT-003", "QT-004", "QT-005", "QT-006", "QT-007"];
    const hasSeedData = state.employees.some(e => defaultIds.includes(e.id));
    if (hasSeedData) {
        state.employees = state.employees.filter(e => !defaultIds.includes(e.id));
        saveStateToStorage();
    }

    // 2. Identify Page context
    const pathname = window.location.pathname;
    const isLandingPage = pathname.endsWith("index.html") || pathname.endsWith("/") || pathname === "";

    // 3. Session Guard redirection
    if (!state.currentUser && !isLandingPage) {
        window.location.href = "index.html?action=login";
        return;
    }

    // 4. If logged in, configure shared layout nodes
    if (state.currentUser) {
        const avatar = document.getElementById("header-user-avatar");
        const nameLabel = document.getElementById("header-user-name");
        
        if (avatar) avatar.textContent = "AD";
        if (nameLabel) nameLabel.textContent = "Admin User";

        // Ticker System Time
        const updateTime = () => {
            const el = document.getElementById("nav-system-time");
            if (el) {
                const now = new Date();
                el.textContent = now.toLocaleDateString() + " | " + now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }
        };
        updateTime();
        setInterval(updateTime, 1000);

        // Sidebar termination trigger
        const logoutBtn = document.getElementById("btn-logout-sidebar");
        if (logoutBtn) {
            logoutBtn.addEventListener("click", () => {
                const settings = state.companySettings || DEFAULT_COMPANY_SETTINGS;
                Auditor.log(`Administrator logged out from ${settings.shortName || "QT Consultancy"} Portal.`);
                state.currentUser = null;
                saveStateToStorage();
                window.location.href = "index.html";
            });
        }
    }
});

function applyCompanyBranding() {
    const settings = state.companySettings || DEFAULT_COMPANY_SETTINGS;

    // 1. Title tag update
    if (settings.shortName) {
        const currentTitle = document.title;
        if (currentTitle.includes("QT Consultancy")) {
            document.title = currentTitle.replace("QT Consultancy", settings.shortName);
        } else if (!currentTitle.includes(settings.shortName)) {
            const parts = currentTitle.split(/[-|]/);
            if (parts.length > 1) {
                parts[0] = settings.shortName + " ";
                document.title = parts.join("-");
            } else {
                document.title = settings.shortName + " - " + currentTitle;
            }
        }
    }

    // 2. Set dynamic theme custom properties on :root
    if (settings.primaryColor) {
        document.documentElement.style.setProperty('--qt-primary', settings.primaryColor);
        document.documentElement.style.setProperty('--primary', settings.primaryColor);
        document.documentElement.style.setProperty('--brand-medium', settings.primaryColor);
    }
    if (settings.sidebarColor) {
        document.documentElement.style.setProperty('--qt-dark', settings.sidebarColor);
        document.documentElement.style.setProperty('--bg-sidebar', settings.sidebarColor);
        document.documentElement.style.setProperty('--brand-dark', settings.sidebarColor);
    }

    // 3. Scan and populate data-company elements
    const elements = document.querySelectorAll('[data-company]');
    elements.forEach(el => {
        const prop = el.getAttribute('data-company');
        if (!prop) return;

        // If the element is an image
        if (el.tagName.toLowerCase() === 'img') {
            if (prop === 'logo') {
                if (settings.logoImage) {
                    el.src = settings.logoImage;
                    el.style.display = '';
                } else {
                    el.src = '';
                    el.style.display = 'none';
                }
            } else if (prop === 'signature') {
                const isInvoicePage = window.location.pathname.includes('/invoices/') || document.getElementById('btn-print-invoice') !== null;
                const isSalarySlipPage = window.location.pathname.includes('/salary-slip/') || document.getElementById('slip-month-header') !== null;
                const applySig = (isInvoicePage && settings.applySignatureToInvoice === false) || (isSalarySlipPage && settings.applySignatureToSalarySlip === false) ? false : true;

                if (applySig && settings.signatureImage) {
                    el.src = settings.signatureImage;
                    el.style.display = '';
                } else {
                    el.src = '';
                    el.style.display = 'none';
                }
            } else if (prop === 'seal') {
                const isInvoicePage = window.location.pathname.includes('/invoices/') || document.getElementById('btn-print-invoice') !== null;
                const isSalarySlipPage = window.location.pathname.includes('/salary-slip/') || document.getElementById('slip-month-header') !== null;
                const applySeal = (isInvoicePage && settings.applySealToInvoice === false) || (isSalarySlipPage && settings.applySealToSalarySlip === false) ? false : true;

                if (applySeal && settings.sealImage) {
                    el.src = settings.sealImage;
                    el.style.display = '';
                } else {
                    el.src = '';
                    el.style.display = 'none';
                }
            }
        } 
        // If it's a link
        else if (el.tagName.toLowerCase() === 'a') {
            el.href = settings[prop] || '#';
            if (el.children.length === 0) {
                el.textContent = settings[prop] !== undefined ? settings[prop] : '';
            }
        }
        // If it's a container element (like a div or span) where we can put HTML or text
        else {
            if (prop === 'logo') {
                if (settings.logoImage) {
                    el.innerHTML = `<img src="${settings.logoImage}" class="w-full h-full object-cover rounded-lg" alt="logo">`;
                } else {
                    el.innerHTML = `<div class="w-full h-full bg-qt-primary text-white flex items-center justify-center font-extrabold rounded-lg text-[0.68rem] leading-none shrink-0">${settings.logoInitials || 'QT'}</div>`;
                }
            } else if (prop === 'signature') {
                const isInvoicePage = window.location.pathname.includes('/invoices/') || document.getElementById('btn-print-invoice') !== null;
                const isSalarySlipPage = window.location.pathname.includes('/salary-slip/') || document.getElementById('slip-month-header') !== null;
                const applySig = (isInvoicePage && settings.applySignatureToInvoice === false) || (isSalarySlipPage && settings.applySignatureToSalarySlip === false) ? false : true;

                if (applySig && settings.signatureImage) {
                    el.innerHTML = `<img src="${settings.signatureImage}" class="h-full w-full object-contain" alt="signature">`;
                } else if (applySig) {
                    // Cursive fallback using signature initials or short name
                    el.innerHTML = `<span class="font-cursive text-xl text-red-650/90 select-none cursor-default leading-none transform rotate-[-2deg]">${settings.shortName}</span>`;
                } else {
                    el.innerHTML = '';
                }
            } else if (prop === 'seal') {
                const isInvoicePage = window.location.pathname.includes('/invoices/') || document.getElementById('btn-print-invoice') !== null;
                const isSalarySlipPage = window.location.pathname.includes('/salary-slip/') || document.getElementById('slip-month-header') !== null;
                const applySeal = (isInvoicePage && settings.applySealToInvoice === false) || (isSalarySlipPage && settings.applySealToSalarySlip === false) ? false : true;

                if (applySeal && settings.sealImage) {
                    el.innerHTML = `<img src="${settings.sealImage}" class="h-full w-full object-contain" alt="seal">`;
                } else if (applySeal) {
                    // Render default SVG stamp seal
                    el.innerHTML = `
                        <svg width="100" height="100" viewBox="0 0 100 100" class="text-blue-700/80 w-full h-full">
                            <circle cx="50" cy="50" r="46" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3.5 1" />
                            <circle cx="50" cy="50" r="43" fill="none" stroke="currentColor" stroke-width="1" />
                            <circle cx="50" cy="50" r="29" fill="none" stroke="currentColor" stroke-width="1" />
                            <path id="seal-text-path-top-dyn" d="M 14 50 A 36 36 0 0 1 86 50" fill="none" />
                            <path id="seal-text-path-bottom-dyn" d="M 86 50 A 36 36 0 0 1 14 50" fill="none" />
                            <text font-size="6" font-weight="900" fill="currentColor" letter-spacing="0.5">
                                <textPath href="#seal-text-path-top-dyn" startOffset="50%" text-anchor="middle">
                                    ${(settings.fullLegalName || 'QT Consultancy').toUpperCase()}
                                </textPath>
                            </text>
                            <text font-size="6" font-weight="900" fill="currentColor" letter-spacing="1">
                                <textPath href="#seal-text-path-bottom-dyn" startOffset="50%" text-anchor="middle">
                                    * ${(settings.headOfficeAddress ? settings.headOfficeAddress.split('\n').pop().split(',')[0].trim().toUpperCase() : 'GURGAON').toUpperCase()} *
                                </textPath>
                            </text>
                            <g transform="translate(50, 50) scale(0.55)" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M -10 -15 C 0 -15, 10 -18, 10 -18 C 10 -18, 10 5, 0 15 C -10 5, -10 -18, -10 -18 Z" />
                                <circle cx="0" cy="-2" r="4" fill="none" stroke="currentColor" stroke-width="1.5" />
                                <line x1="2" y1="0" x2="6" y2="4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
                            </g>
                        </svg>
                    `;
                } else {
                    el.innerHTML = '';
                }
            } else if (prop === 'headOfficeAddress' || prop === 'address') {
                el.innerHTML = (settings.headOfficeAddress || '').replace(/\n/g, '<br>');
            } else {
                el.textContent = settings[prop] !== undefined ? settings[prop] : '';
            }
        }
    });

    // 4. Update the Brand Name in Sidebar & Brand Logo in Sidebar for pages that have sidebar
    const brandNameSpans = document.querySelectorAll("aside span.text-white, aside span.text-white\\/90, aside .sidebar-brand-name");
    brandNameSpans.forEach(span => {
        span.textContent = settings.shortName;
    });

    const sidebarBrandBlock = document.querySelector("aside div.flex.items-center.gap-2\\.5, aside div.flex.items-center.justify-between, aside div.flex.items-center");
    if (sidebarBrandBlock) {
        const logoTarget = sidebarBrandBlock.querySelector("div.w-8.h-8, img#brand-logo-img, div#brand-logo-div, svg.shrink-0");
        if (logoTarget) {
            if (settings.logoImage) {
                logoTarget.outerHTML = `<img src="${settings.logoImage}" id="brand-logo-img" data-company="logo" class="w-8 h-8 rounded-lg object-cover shrink-0" alt="logo">`;
            } else {
                logoTarget.outerHTML = `<div id="brand-logo-div" data-company="logo" class="w-8 h-8 bg-qt-medium rounded-lg flex items-center justify-center text-white font-extrabold text-sm shrink-0">${settings.logoInitials || 'QT'}</div>`;
            }
        }
    }

    // 5. Update favicon dynamically if logo exists
    const favicon = document.querySelector('link[rel="icon"], link[rel="shortcut icon"]');
    if (favicon && settings.logoImage) {
        favicon.href = settings.logoImage;
    }

    // 6. Update meta description dynamically if it exists
    if (settings.shortName) {
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            metaDesc.setAttribute('content', `${settings.shortName} provides strategic HR solutions, Pan-India recruitment, payroll compliance, and manpower migration.`);
        }
    }
}

// Global synchronization listener across tabs / windows
window.addEventListener('storage', (e) => {
    if (e.key === 'qt_consultancy_state') {
        loadStateFromStorage();
        applyCompanyBranding();
        
        // Context-aware UI redraws
        if (typeof recalculateInvoice === 'function') {
            recalculateInvoice();
        }
        if (typeof loadPayslipPreview === 'function' && state.selectedEmployee) {
            loadPayslipPreview(state.selectedEmployee.id);
        }
        if (typeof renderEmployees === 'function') {
            renderEmployees();
        }
        if (typeof renderPayrollMatrix === 'function') {
            renderPayrollMatrix();
        }
        if (typeof renderSelectionList === 'function') {
            renderSelectionList();
        }
    }
});

// Global Toggle Sidebar Function for Mobile Drawer Layout
function toggleSidebar() {
    const sidebar = document.getElementById("app-sidebar");
    const overlay = document.getElementById("sidebar-overlay");
    if (sidebar) {
        if (sidebar.classList.contains("-translate-x-full")) {
            sidebar.classList.remove("-translate-x-full");
            if (overlay) {
                overlay.classList.remove("hidden");
            }
        } else {
            sidebar.classList.add("-translate-x-full");
            if (overlay) {
                overlay.classList.add("hidden");
            }
        }
    }
}
