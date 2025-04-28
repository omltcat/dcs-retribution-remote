if RetCtrl then return end

RetCtrl = {}

---Chat commands to control the server
---@param playerID integer
---@param message string
---@param all boolean
function RetCtrl.onPlayerTrySendChat(playerID, message, all)
    if message:sub(1, 1) ~= "/" then return end

    message = message:lower()
    if message == "/resume" then
        DCS.setPause(false)
    elseif message == "/pause" then
        DCS.setPause(true)
    end
end

DCS.setUserCallbacks(RetCtrl)
log.info("Retribution Remote Control Script loaded")