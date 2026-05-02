<x-layouts.app title="Register">
    <section class="auth-panel">
        <div class="auth-copy">
            <span class="eyebrow">Access control</span>
            <h1>Create a dashboard account</h1>
            <p>The first registered account becomes admin automatically. Later accounts start as users until an admin changes their role.</p>
        </div>

        <form class="auth-card" method="POST" action="{{ route('register') }}">
            @csrf
            <h2>Register</h2>
            @include('partials.errors')

            <label>
                Name
                <input name="name" type="text" value="{{ old('name') }}" autocomplete="name" required autofocus>
            </label>

            <label>
                Email
                <input name="email" type="email" value="{{ old('email') }}" autocomplete="email" required>
            </label>

            <label>
                Password
                <input name="password" type="password" autocomplete="new-password" required>
            </label>

            <label>
                Confirm password
                <input name="password_confirmation" type="password" autocomplete="new-password" required>
            </label>

            <button class="primary-button" type="submit">Create account</button>

            <p class="form-note">Already registered? <a href="{{ route('login') }}">Sign in</a></p>
        </form>
    </section>
</x-layouts.app>
