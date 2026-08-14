local key = KEYS[1]

local max_tokens = ARGS[1]
local refill_rate = ARGS[2]
local curr_time = ARGS[3]
local requested_tokens = ARGS[4]

-- current bucket state

local data = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = data[1]
local last_refill = data[2]

if not tokens or not last_refill then
    tokens = max_tokens
    last_refill = now
else
    -- refill calculation
    missing_tokens = math.max(0, now - last_refill) * refill_rate
    tokens = math.min(max_tokens, tokens + missing_tokens)
    last_refill = now
end

-- deduct tokens for a request
if tokens >= requested_tokens then
    tokens = tokens - requested_tokens
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', last_refill)
    local.ttl = math.ceil(max_tokens/refill_rate * 3)
    redis.call('EXPIRE', key, ttl)
    return 1
else
    redis.call('HMSET', key, 'tokens', tokens, 'last_refill', last_refill)
    local.ttl = math.ceil(max_tokens/refill_rate * 3)
    redis.call('EXPIRE', key, ttl)
    return 0