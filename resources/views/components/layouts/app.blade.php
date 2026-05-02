<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title ?? 'Violence Detection Dashboard' }}</title>
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
            @if(session('status'))
                <div class="flash">{{ session('status') }}</div>
            @endif

            {{ $slot }}
        </main>
    </div>
</body>
</html>
