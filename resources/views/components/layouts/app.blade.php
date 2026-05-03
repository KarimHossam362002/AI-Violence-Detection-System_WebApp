<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title ?? 'Violence Detection Dashboard' }}</title>
    <script>
        (() => {
            const savedTheme = localStorage.getItem('theme');
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.dataset.theme = savedTheme || (prefersDark ? 'dark' : 'light');
        })();
    </script>
    @viteReactRefresh
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body>
    <div class="app-shell">
        @auth
            <aside class="sidebar">
                <a class="brand" href="{{ route('dashboard') }}">
                    <span class="brand-mark">VD</span>
                    <span>
                        <strong>Vision Desk</strong>
                        <small>Operator Console</small>
                    </span>
                </a>

                <nav class="nav-list">
                    <a @class(['active' => request()->routeIs('dashboard')]) href="{{ route('dashboard') }}">Dashboard</a>
                    @if(auth()->user()->isAdmin())
                        <a @class(['active' => request()->routeIs('admin.*')]) href="{{ route('admin.users.index') }}">Users</a>
                    @endif
                </nav>

                <div class="sidebar-footer">
                    <div>
                        <strong>{{ auth()->user()->name }}</strong>
                        <small>{{ ucfirst(auth()->user()->role) }}</small>
                    </div>
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button class="ghost-button" type="submit">Logout</button>
                    </form>
                </div>
            </aside>
        @endauth

        <main class="main-content">
            @guest
                <button class="theme-icon-button floating-theme-toggle" type="button" data-theme-toggle aria-label="Switch to dark mode">
                    <svg class="theme-icon theme-icon-dark" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M21 14.5A8.5 8.5 0 0 1 9.5 3 7 7 0 1 0 21 14.5Z" />
                    </svg>
                    <svg class="theme-icon theme-icon-light" viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M12 4V2m0 20v-2m8-8h2M2 12h2m13.66-5.66 1.41-1.41M4.93 19.07l1.41-1.41m0-11.32L4.93 4.93m14.14 14.14-1.41-1.41" />
                        <circle cx="12" cy="12" r="4" />
                    </svg>
                </button>
            @endguest

            @if(session('status'))
                <div class="flash">{{ session('status') }}</div>
            @endif

            {{ $slot }}
        </main>
    </div>
    <script>
        (() => {
            const setTheme = (theme) => {
                document.documentElement.dataset.theme = theme;
                localStorage.setItem('theme', theme);

                document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
                    button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
                });
            };

            setTheme(document.documentElement.dataset.theme || 'light');

            document.addEventListener('click', (event) => {
                const button = event.target.closest('[data-theme-toggle]');

                if (!button) {
                    return;
                }

                setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
            });
        })();
    </script>
</body>
</html>
