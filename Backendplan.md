# Coffee Backend Architecture Plan

## Summary

Build the backend directly in the project root with this long-term structure:

```text
Coffee/
  manage.py
  config/
    settings.py
    urls.py
    asgi.py
    wsgi.py
  apps/
    core/
    users/
    catalog/
    blog/
    sales/
    orders/
    payments/
    reviews/
    newsletter/
  frontend/
  media/
```

This backend is wholesale-first, quote-based, React-ready, and production-minded. It will expose a versioned REST API at `/api/v1/`, use Django admin as the operational back office, use a custom user model, keep marketing page presentation in the frontend for now, and support a future move into fuller retail commerce without redesigning the core data model.

## Implementation Phases

1. **Foundation**
   - Rename the Django config package from `coffee` to `config`.
   - Keep a single `config/settings.py` as requested.
   - Add `apps/` and register all Django apps with `apps.<app_name>`.
   - Configure `SQLite` for development and `MySQL` for production via environment variables.
   - Add shared `core` pieces: timestamped base model, soft-delete/status helpers if needed, health check endpoint, shared constants, email/storage helpers.

2. **Users and Auth**
   - Create `users` with a custom user model from day one.
   - Use staff/admin access through Django admin and session auth.
   - Use JWT for customer-facing API auth.
   - Support guest inquiry flows plus optional customer accounts for future quote/order history.
   - Add profile fields needed for buyers/customers without overloading the auth model.

3. **Catalog**
   - Create a unified catalog in `catalog`, not separate wholesale and retail systems.
   - Core types: `Product`, `ProductVariant`, `ProductImage`, `Category`, `WholesaleOffer`, `InventoryRecord`.
   - `Product` stays shared; `ProductVariant` supports future retail packaging/options; `WholesaleOffer` carries wholesale-specific terms like MOQ, grade, quote-only flags, buyer notes, and availability.
   - Use quote-based pricing publicly for wholesale products.
   - Support numeric stock where useful plus availability states for lots or inquiry-only items.

4. **Blog**
   - Create `blog` with `Post`, `Category`, `Tag`, and author linkage.
   - Include slug, summary, featured image, SEO title/meta description, draft/published status, and publish date.
   - Expose public read APIs for published content and staff CRUD in admin/API.

5. **Sales, Orders, and Shipping**
   - Create `sales` for the wholesale journey: `Inquiry`, `InquiryItem`, `Quote`, `QuoteItem`, `QuoteStatus`.
   - Primary flow: inquiry -> staff review -> quote -> accepted quote -> order conversion.
   - Create `orders` for `Order`, `OrderItem`, `Address`, and fulfillment/shipping fields.
   - Shipping stays `quoted + fulfillment`: store addresses, preferred shipping details, quoted shipping amount, fulfillment state, tracking/reference notes.
   - Do not implement live carrier-rate integrations in the initial backend plan.

6. **Payments**
   - Create `payments` with `Payment`, `PaymentAttempt`, and provider references.
   - Build payment abstraction only: provider enum/interface, transaction state machine, webhook endpoint placeholders, and order/quote linkage.
   - Do not wire Stripe or Paystack yet, but design the adapter layer so either can be added without schema redesign.

7. **Reviews and Newsletter**
   - Create `reviews` for customer product reviews, not just curated testimonials.
   - Review submission should be customer-facing, but publication must be staff moderated.
   - Create `newsletter` for email subscriptions and opt-in tracking.
   - Keep marketing homepage/about/gallery content in frontend code for now; only blog and product-related content are admin-managed initially.

8. **Permissions and API Surface**
   - Use `Public Read + Staff CRUD` as the default permission model.
   - Public: blog list/detail, catalog list/detail, allowed guest forms like inquiries and newsletter signup.
   - Customer-authenticated: profile access, own quote/order history later, allowed review submission.
   - Staff-only: full CRUD for blog, catalog, quotes, orders, reviews moderation, newsletter admin, and payment oversight.

9. **Operational Features**
   - Add core transactional emails: inquiry received, quote sent, quote accepted, order status updates, and account actions.
   - Use USD as the system currency.
   - Keep order/quote totals tax-ready with subtotal, tax, shipping, discount if needed, and grand total fields.
   - Use local file storage for uploaded media as requested.

10. **Testing and Hardening**
   - Standardize on `pytest`.
   - Add API, model, permission, and workflow tests before considering the backend complete.
   - Treat “done” as end-to-end verified behavior, not only model creation.

## Public APIs and Key Interfaces

- Base path: `/api/v1/`
- Auth: JWT endpoints for customer auth; Django admin/session for staff
- Catalog: public read endpoints for products, variants, categories, and wholesale availability
- Blog: public read endpoints for published posts, categories, tags
- Sales: guest inquiry creation; staff quote management; quote-to-order conversion
- Orders: customer/staff order endpoints with strict object ownership rules
- Payments: internal/provider-facing payment endpoints and webhook stubs
- Reviews: public read for approved reviews; authenticated customer submission; staff moderation
- Newsletter: guest subscription endpoint; staff management endpoint

## Test Plan

- Config loads correctly in development and production-style environments.
- Custom user model works with admin, JWT auth, and permissions.
- Public catalog and blog endpoints return only allowed data.
- Guest inquiry submission works and triggers expected email/status behavior.
- Staff can create a quote from an inquiry and convert an accepted quote into an order.
- Orders compute subtotal, tax-ready totals, shipping, and status changes correctly.
- Payment records transition cleanly through pending/succeeded/failed/cancelled states.
- Customer reviews require moderation before public visibility.
- Staff-only CRUD endpoints reject public/customer access.
- MySQL-safe behavior is preserved by avoiding SQLite-only assumptions.

## Assumptions and Defaults

- Root-level backend is preferred; no separate `backend/` directory.
- `config/` replaces the current Django project package name.
- Single `config/settings.py` is intentional for simplicity.
- Wholesale is the primary business model; retail readiness is supported through the unified catalog but not surfaced first.
- Pricing is quote-based for wholesale; public retail-style checkout is not the initial commerce surface.
- Guest users can submit inquiries; customer accounts are optional but supported.
- Marketing page sections outside blog/products remain frontend-managed for now.
- Media storage stays local-file based unless you later choose to switch to cloud storage.
