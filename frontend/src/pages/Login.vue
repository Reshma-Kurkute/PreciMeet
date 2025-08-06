<!-- <template>
  <div class="m-3 flex flex-row items-center justify-center">
    <Card title="Login to your PreciMeet App!" class="w-full max-w-md mt-4">
      <form class="flex flex-col space-y-2 w-full" @submit.prevent="submit">
        <Input
          required
          name="email"
          type="text"
          placeholder="johndoe@email.com"
          label="User ID"
        />
        <Input
          required
          name="password"
          type="password"
          placeholder="••••••"
          label="Password"
        />
        <Button :loading="session.login.loading" variant="solid">Login</Button>
      </form>
    </Card>
  </div>
</template>

<script lang="ts" setup>
import { session } from '../data/session'

function submit(e) {
  let formData = new FormData(e.target)
  session.login.submit({
    email: formData.get('email'),
    password: formData.get('password'),
  })
}
</script> -->
<template>
  <div class="m-3 flex flex-row items-center justify-center">
    <!-- Glow Shadow Effect -->
    <div
      id="shadow"
      class="fixed top-0 left-0 z-10 h-32 w-32 rounded-full bg-white blur-[70px] transition-opacity duration-300 opacity-0"
    ></div>

    <!-- Card Container -->
    <div
      id="card"
      class="radius-xl relative z-20 flex h-screen w-full flex-col overflow-auto p-5 sm:p-10"
    >
      <div
        class="relative mx-auto my-auto w-full max-w-md shrink-0 overflow-hidden rounded-4xl border-t border-white/20 bg-gradient-to-t from-zinc-100/10 to-zinc-950/50 to-50% p-8 text-white shadow-2xl shadow-black outline -outline-offset-1 outline-white/5 backdrop-blur-2xl"
      >
        <h2 class="mb-7 text-[1.4rem] font-medium text-center">PreciMeet</h2>

        <!-- Login Form -->
        <form @submit.prevent="submit" class="flex flex-col gap-4 text-sm sm:grid grid-cols-2">
          <!-- Email -->
          <div class="relative col-span-2 h-11 overflow-hidden">
            <label for="email" class="sr-only">User ID</label>
            <input
              id="email"
              name="email"
              type="text"
              required
              class="peer relative z-1 h-full w-full rounded-md border border-white/8 bg-white/5 pr-4 pl-11 placeholder:text-white/30 focus:outline-0"
              placeholder="Enter your email"
            />
          </div>

          <!-- Password -->
          <div class="relative col-span-2 h-11 overflow-hidden">
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              required
              class="peer relative z-1 h-full w-full rounded-md border border-white/8 bg-white/5 pr-4 pl-11 placeholder:text-white/30 focus:outline-0"
              placeholder="Enter your password"
            />
          </div>

          <!-- Login Button -->
          <div class="col-span-2">
            <button
              type="submit"
              :disabled="session.login.loading"
              class="mt-4 h-12 w-full rounded-md bg-white text-sm font-medium text-zinc-800 shadow-xl transition hover:brightness-110 disabled:opacity-50"
            >
              <span v-if="session.login.loading">Logging in...</span>
              <span v-else>Login</span>
            </button>
          </div>
        </form>

        <!-- Subtle Glow Accent -->
        <div class="absolute inset-x-32 -bottom-20 left-32 h-10 bg-white blur-2xl"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { session } from '../data/session'

function submit(e: Event) {
  const formData = new FormData(e.target as HTMLFormElement)
  const email = formData.get('email')
  const password = formData.get('password')

  session.login.submit({ email, password })
}

onMounted(() => {
  const shadow = document.getElementById('shadow')
  const card = document.getElementById('card')

  if (!shadow || !card) return

  document.body.addEventListener('mousemove', (e) => {
    const { clientX, clientY } = e
    if ((e.target as HTMLElement).closest('#card')) {
      shadow.style.transform = `translateX(${clientX - 60}px) translateY(${clientY - 60}px)`
      shadow.style.opacity = '0.5'
    } else {
      shadow.style.opacity = '0'
    }
  })
})
</script>
