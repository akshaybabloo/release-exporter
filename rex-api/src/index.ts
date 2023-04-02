import {Hono} from 'hono'
import {KVNamespace} from '@cloudflare/workers-types'

type Bindings = {
	GOLLAHALLI_KV: KVNamespace;
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/', async (c, next) => {
    const a = await c.env.GOLLAHALLI_KV.list();
    return c.text('Hello World!');
})

export default app
