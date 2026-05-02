<x-layouts.app title="Login">
    <section class="auth-panel">
        <div class="auth-copy">
            <span class="eyebrow">Secure monitoring</span>
            <h1>Sign in to the operator dashboard</h1>
            <p>Review live camera access, model incidents, saved evidence clips, and high-priority alerts from one console.</p>
        </div>

        <form class="auth-card" method="POST" action="{{ route('login') }}">
            @csrf
            <h2>Login</h2>
            @include('partials.errors')

            <label>
                Email
                <input name="email" type="email" value="{{ old('email') }}" autocomplete="email" required autofocus>
            </label>

            <label>
                Password
                <input name="password" type="password" autocomplete="current-password" required>
            </label>

            <label class="check-row">
                <input name="remember" type="checkbox" value="1">
                Remember me
            </label>

            <button class="primary-button" type="submit">Sign in</button>

            <p class="form-note">No account yet? <a href="{{ route('register') }}">Create one</a></p>
        </form>
    </section>
</x-layouts.app>
