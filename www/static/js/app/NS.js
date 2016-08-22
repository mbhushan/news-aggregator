if (!window.NationStory) {
    window.NationStory = {};
    window.NS = window.NationStory;
};

NationStory.notify = function(message, type) {
    $.notify(message, type);
};

NationStory.util = {
    toTitleCase : function(str) {
        return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    }
};
