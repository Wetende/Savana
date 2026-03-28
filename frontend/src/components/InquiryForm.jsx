import { useState } from 'react'
import { businessTypes, initialInquiry, volumeOptions } from '../content/siteContent.js'

function validateInquiry(form) {
  const errors = {}

  if (!form.fullName.trim()) {
    errors.fullName = 'Full name is required.'
  }

  if (!form.companyName.trim()) {
    errors.companyName = 'Company name is required.'
  }

  if (!form.email.trim()) {
    errors.email = 'Email is required.'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Enter a valid business email address.'
  }

  if (!form.message.trim()) {
    errors.message = 'Tell us what you need so we can reply with the right pricing context.'
  }

  return errors
}

function InquiryForm() {
  const [form, setForm] = useState(initialInquiry)
  const [errors, setErrors] = useState({})
  const [status, setStatus] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  const handleChange = (event) => {
    const { name, value } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))

    setErrors((current) => {
      if (!current[name]) {
        return current
      }

      const nextErrors = { ...current }
      delete nextErrors[name]
      return nextErrors
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    const nextErrors = validateInquiry(form)

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors)
      setStatus({
        type: 'error',
        message: 'Please complete the required fields before submitting your inquiry.',
      })
      return
    }

    setSubmitting(true)
    setStatus(null)

    window.setTimeout(() => {
      setSubmitting(false)
      setErrors({})
      setForm(initialInquiry)
      setStatus({
        type: 'success',
        message:
          'Thanks. This wholesale inquiry form is UI-complete for v1. In production it should connect to your sales inbox or CRM.',
      })
    }, 850)
  }

  return (
    <form className="inquiry-form" noValidate onSubmit={handleSubmit}>
      <div className="form-grid">
        <label className="field">
          <span>Full name</span>
          <input
            name="fullName"
            type="text"
            value={form.fullName}
            onChange={handleChange}
            aria-invalid={Boolean(errors.fullName)}
            placeholder="Your full name"
          />
          {errors.fullName ? <small>{errors.fullName}</small> : null}
        </label>

        <label className="field">
          <span>Company name</span>
          <input
            name="companyName"
            type="text"
            value={form.companyName}
            onChange={handleChange}
            aria-invalid={Boolean(errors.companyName)}
            placeholder="Company or buying group"
          />
          {errors.companyName ? <small>{errors.companyName}</small> : null}
        </label>

        <label className="field">
          <span>Business type</span>
          <select name="businessType" value={form.businessType} onChange={handleChange}>
            {businessTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>

        <label className="field">
          <span>Business email</span>
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            aria-invalid={Boolean(errors.email)}
            placeholder="name@company.com"
          />
          {errors.email ? <small>{errors.email}</small> : null}
        </label>

        <label className="field">
          <span>Phone number</span>
          <input
            name="phone"
            type="tel"
            value={form.phone}
            onChange={handleChange}
            placeholder="Optional"
          />
        </label>

        <label className="field">
          <span>Estimated monthly volume</span>
          <select name="monthlyVolume" value={form.monthlyVolume} onChange={handleChange}>
            <option value="">Select volume range</option>
            {volumeOptions.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
      </div>

      <label className="field field-full">
        <span>Inquiry details</span>
        <textarea
          name="message"
          rows="6"
          value={form.message}
          onChange={handleChange}
          aria-invalid={Boolean(errors.message)}
          placeholder="Tell us which coffee profile, buyer channel, or pricing conversation you want to start."
        />
        {errors.message ? <small>{errors.message}</small> : null}
      </label>

      <div className="form-actions">
        <button className="button button-primary" type="submit" disabled={submitting}>
          {submitting ? 'Preparing Inquiry...' : 'Request Wholesale Pricing'}
        </button>
        <p className="form-note">
          Your inquiry goes directly to our wholesale team. We typically respond within 24–48 hours.
        </p>
      </div>

      {status ? (
        <div className={`form-status ${status.type === 'success' ? 'is-success' : 'is-error'}`}>
          {status.message}
        </div>
      ) : null}
    </form>
  )
}

export default InquiryForm
