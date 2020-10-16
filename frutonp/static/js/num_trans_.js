NUMBER_MAP = {
    "0": "०",
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
var NumberTranslator = {
    currentLanguage: getCookie('django_language'),
    translateToNep: function translator(value){
        value = `${value}`;
        var translated_value = "";
        if(this.currentLanguage == "ne"){
            for(var i=0; i<value.length; i++){
                try {
                    translated_value+=NUMBER_MAP[value[i]];
                } catch (e) {
                    translated_value+=value[i];
                }
            }
            return translated_value;
        }
        return value;
    },
    translateToEng: function translator(value){
        var translated_value = "";
        for(var i=0; i<value.length; i++){
            try {
                translated_value+=this._getKeyByValue(value[i]);
            } catch (e) {
                translated_value+=value[i];
            }
        }
        return translated_value;
    },
    _getKeyByValue: function getKeyByValue(value) {
        return Object.keys(NUMBER_MAP).find(key => NUMBER_MAP[key] === value);
    }
}