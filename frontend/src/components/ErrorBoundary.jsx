import { Component } from 'react';
import { Link } from 'react-router-dom';

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error('A page failed to render', error, info?.componentStack);
  }

  componentDidUpdate(previousProps) {
    if (this.state.hasError && previousProps.resetKey !== this.props.resetKey) {
      this.setState({ hasError: false });
    }
  }

  render() {
    if (!this.state.hasError) {
      return this.props.children;
    }

    return (
      <div className="mx-auto max-w-xl rounded-xl border border-rose-200 bg-rose-50 p-6 text-center shadow-sm">
        <p className="text-[10px] font-semibold uppercase tracking-[0.24em] text-rose-700">
          Something went wrong
        </p>
        <h2 className="mt-2 text-xl font-semibold tracking-tight text-stone-900">
          This page could not be displayed
        </h2>
        <p className="mt-2 text-sm leading-relaxed text-stone-600">
          Your data is safe. Reload the page or return to the dashboard to keep
          working.
        </p>
        <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
          <button
            type="button"
            onClick={() => window.location.reload()}
            className="rounded-lg bg-stone-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-stone-800"
          >
            Reload page
          </button>
          <Link
            to="/"
            onClick={() => this.setState({ hasError: false })}
            className="rounded-lg border border-stone-300 bg-white px-4 py-2 text-sm font-medium text-stone-700 transition hover:border-teal-400 hover:text-teal-800"
          >
            Back to dashboard
          </Link>
        </div>
      </div>
    );
  }
}
