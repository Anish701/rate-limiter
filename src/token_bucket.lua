local key = KEYS[1]

local max_tokens = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local curr_time = tonumber(ARGV[3])
local requested_tokens = tonumber(ARGV[4])

-- current bucket state
local data = redis.call('HMGET', key, 'tokens', 'last_refill')
local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

if not tokens or not last_refill then
    tokens = max_tokens
    last_refill = curr_time
else
    -- refill calculation
    local missing_tokens = math.max(0, curr_time - last_refill) * refill_rate
    tokens = math.min(max_tokens, tokens + missing_tokens)
    last_refill = curr_time
end

local allowed = 0

-- approve request if enough tokens
if tokens >= requested_tokens then
    tokens = tokens - requested_tokens
    allowed = 1
end

-- update bucket state
redis.call('HSET', key, 'tokens', tokens, 'last_refill', last_refill)

local ttl = math.ceil((max_tokens / refill_rate) * 3)
redis.call('EXPIRE', key, ttl)

return allowed