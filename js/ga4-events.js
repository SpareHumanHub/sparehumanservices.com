/* Spare Human Services — GA4 conversion tracking (Sept 2026)
   Fires: click_to_call, click_to_email, book_click, review_intent
   (generate_lead fires inline on intake.html success; begin_booking inline on book.html) */
(function () {
  function gtag() { window.dataLayer = window.dataLayer || []; window.dataLayer.push(arguments); }

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a') : null;
    if (!a) return;
    var href = (a.getAttribute('href') || '').trim();
    var label = (a.textContent || '').trim().slice(0, 60);

    if (href.indexOf('tel:') === 0) {
      gtag('event', 'click_to_call', { event_category: 'engagement', event_label: href });
    } else if (href.indexOf('mailto:') === 0) {
      gtag('event', 'click_to_email', { event_category: 'engagement', event_label: href });
    } else if (/\/book(\.html)?([?#]|$)/.test(href)) {
      gtag('event', 'book_click', { event_category: 'conversion', event_label: label, source_page: location.pathname });
    } else if (/maps\.google|google\.com\/maps|goo\.gl\/maps|g\.page\./.test(href)) {
      gtag('event', 'review_intent', { event_category: 'conversion', event_label: href.slice(0, 120) });
    }
  }, true);
})();
