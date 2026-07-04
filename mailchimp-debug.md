# Mailchimp Debug

## Goal

Find out what's injecting `chimpstatic.com/mcjs-connected/...` into the page.

### Possible Sources

**Apps list**

I see mailchimp in the apps list but it's not set up. there is a message that says "Enable the Mailchimp App Embed to complete your setup and enable signup forms"

**Confirm it's the injector**

here are the two elements that are called "chimpstatic":

<script type="text/javascript" async="" src="https://chimpstatic.com/mcjs-connected/js/users/bb68751aca24eb8005a87da31/d9aa649c0e2ad063e057bdd8c.js?shop=hazelboutiquenj.myshopify.com"></script>

(function() {
  var isLoaded = false;
  function asyncLoad() {
    if (isLoaded) return;
    isLoaded = true;
    var urls = ["https:\/\/popup4.lifterpopup.com\/js\/modal.js?shop=hazelboutiquenj.myshopify.com","https:\/\/s3-us-west-2.amazonaws.com\/da-restock\/da-restock.js?shop=hazelboutiquenj.myshopify.com","https:\/\/cdn.fera.ai\/js\/fera.placeholder.js?shop=hazelboutiquenj.myshopify.com","https:\/\/d10lpsik1i8c69.cloudfront.net\/w.js?shop=hazelboutiquenj.myshopify.com","https:\/\/shopify-widget.route.com\/shopify.widget.js?shop=hazelboutiquenj.myshopify.com","https:\/\/chimpstatic.com\/mcjs-connected\/js\/users\/bb68751aca24eb8005a87da31\/d9aa649c0e2ad063e057bdd8c.js?shop=hazelboutiquenj.myshopify.com","https:\/\/cdn.hextom.com\/js\/freeshippingbar.js?shop=hazelboutiquenj.myshopify.com","\/\/backinstock.useamp.com\/widget\/14787_1783058685.js?category=bis\u0026v=6\u0026shop=hazelboutiquenj.myshopify.com"];
    for (var i = 0; i < urls.length; i++) {
      var s = document.createElement('script');
      s.type = 'text/javascript';
      s.async = true;
      s.src = urls[i];
      var x = document.getElementsByTagName('script')[0];
      x.parentNode.insertBefore(s, x);
    }
  };
  if(window.attachEvent) {
    window.attachEvent('onload', asyncLoad);
  } else {
    window.addEventListener('load', asyncLoad, false);
  }
})();


When i click oj tthe first one, i get this:

"/* eslint-disable */
(function () {
    /* eslint-disable */
    if (!window.$mcSite) {
        $mcSite = {
            optinFeatures: [],

            loadingPrerequisites: [],
            permissionProviders: {},

            registerPermissionProvider: function (permission, permissionResolutionPromise) {
                window.$mcSite.permissionProviders[permission] = permissionResolutionPromise;
            },

            enableOptIn: function () {
                this.createCookie("mc_user_optin", true, 365);
                this.optinFeatures.forEach(function (fn) {
                    fn();
                });
            },

            runIfOptedIn: function (fn, additionalPermissions) {
                Promise.all(this.loadingPrerequisites).then(function () {
                    this._runIfOptedIn.call(this, fn, additionalPermissions);
                }.bind(this));
            },

            _runIfOptedIn: function (fn, additionalPermissions) {
                if (!additionalPermissions || additionalPermissions.length === 0) {
                    if (this.hasOptedIn()) {
                        fn();
                    } else {
                        this.optinFeatures.push(fn);
                    }
                } else {
                    var wrappedPermmissionsFn = function () {
                        if (additionalPermissions.length === 0) {
                            fn();
                        }

                        // Get available permission providers
                        var permissionProviders = additionalPermissions.reduce(function (providers, permission) {
                            if (window.$mcSite.permissionProviders[permission]) {
                                providers.push(window.$mcSite.permissionProviders[permission]);
                            }
                            return providers;
                        }, []);

                        // Check if all permissions are granted
                        Promise.all(permissionProviders).then(function (results) {
                            var allPermissionsGranted = results.every(function (result) {
                                return result === true;
                            });

                            if (allPermissionsGranted) {
                                fn();
                            }
                        });
                    }

                    if (this.hasOptedIn()) {
                        wrappedPermmissionsFn();
                    } else {
                        this.optinFeatures.push(wrappedPermmissionsFn);
                    }
                }
            },

            hasOptedIn: function () {
                var cookieValue = this.readCookie("mc_user_optin");

                if (cookieValue === undefined) {
                    return true;
                }

                return cookieValue === "true";
            },

            createCookie: function (name, value, expirationDays) {
                var cookie_value = encodeURIComponent(value) + ";";

                if (expirationDays === undefined) {
                    throw new Error("expirationDays is not defined");
                }

                // set expiration
                if (expirationDays !== null) {
                    var expirationDate = new Date();
                    expirationDate.setDate(expirationDate.getDate() + expirationDays);
                    cookie_value += " expires=" + expirationDate.toUTCString() + ";";
                }

                cookie_value += "path=/";
                document.cookie = name + "=" + cookie_value;
            },

            readCookie: function (name) {
                var nameEQ = name + "=";
                var ca = document.cookie.split(";");

                for (var i = 0; i < ca.length; i++) {
                    var c = ca[i];

                    while (c.charAt(0) === " ") {
                        c = c.substring(1, c.length);
                    }

                    if (c.indexOf(nameEQ) === 0) {
                        return c.substring(nameEQ.length, c.length);
                    }
                }

                return undefined;
            }
        };
    }

    /* eslint-disable */
(function () {
    var availablePermissionResolvers = {
        'preferencesProcessingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.preferencesProcessingAllowed();
                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.preferencesAllowed) {
                            resolve(event.detail.preferencesAllowed);
                        }
                    });
                }
            })
        },

        'analyticsProcessingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.analyticsProcessingAllowed();

                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.analyticsAllowed) {
                            resolve(event.detail.analyticsAllowed);
                        }
                    });
                }

            })
        },
        'marketingAllowed': function () {
            return new Promise(function (resolve) {
                try {
                    var result = window.Shopify.customerPrivacy.marketingAllowed();

                    if (!result) {
                        throw new Error('Preferences processing not allowed');
                    }

                    resolve(result);
                } catch (e) {
                    document.addEventListener('visitorConsentCollected', function (event) {
                        if (event.detail && event.detail.marketingAllowed) {
                            resolve(event.detail.marketingAllowed);
                        }
                    });
                }
            })
        }
    };

    /* eslint-disable */
    if (window.$mcSite) {
        if (window.Shopify) {
            window.$mcSite.loadingPrerequisites.push(new Promise(function (resolve) {
                try {
                    window.Shopify.loadFeatures([
                        {
                            name: 'consent-tracking-api',
                            version: '0.1',
                        },
                    ],
                        function () {
                            if (window.Shopify.customerPrivacy) {

                                // Register the permission providers
                                var availablePermissions = Object.keys(availablePermissionResolvers);
                                for (var i = 0; i < availablePermissions.length; i++) {
                                    var permission = availablePermissions[i];

                                    window.$mcSite.registerPermissionProvider(permission, availablePermissionResolvers[permission]());
                                }
                            }
                            resolve();
                        }
                    );
                } catch (e) {
                    resolve();
                }
            }));
        }
    }
})();


    $mcSite.shopify_attribution_cookie={settings:{}};$mcSite.popup_form={settings:{base_url:"mc.us20.list-manage.com",list_id:"7488b9bad0",uuid:"bb68751aca24eb8005a87da31",f_id:"775492",skip_install:""}};$mcSite.amped_forms={settings:{uid:"125022538",src:"https:\/\/form-assets.mailchimp.com\/snippet\/account\/",site_unique_id:"d9aa649c0e2ad063e057bdd8c"}};$mcSite.pixel={settings:{domain:"mcjs.prd.a.intuit.com",version:"1.22.0",apiUrl:"https:\/\/chimpstatic.com\/pixel",autoTrack:"false",context_referenceSystem:"SHOPIFY",context_mailchimpUserId:"125022538",context_mailchimpAudienceId:"115977",context_mailchimpForeignStoreId:"store_ptoo2xtixf17lgoqku3o",context_publicConnectedSiteId:"d9aa649c0e2ad063e057bdd8c"}};
})();
/**
 * This file contains code that will maintain an MC cookie on a Shopify store's site.
 * The cookie stores data from our tracking params (utm_*, mc_* params) to then be
 * attributed to an order during the Shopify checkout process and allow us to have
 * more flexibility in conversion attribution for our outreaches (campaigns, ads, etc).
 */
(function () {
    /**
     * A namespace for MC for Shopify's conversion attribution.
     * @namespace
     */
    var conversion = {
        /**
         * Looks for MC tracking params, validates their values, then stores them in a cookie.
         */
        processParameters: function () {
            var utmCampaignParam = this.getParameter("utm_campaign");
            var utmSourceParam = this.getParameter("utm_source");
            var utmMediumParam = this.getParameter("utm_medium");
            var gclid = this.getParameter("gclid");
            var mccid = this.getParameter("mc_cid");

            if (this.isValidUTMCampaign(utmCampaignParam) &&
                this.isValidUTMSource(utmSourceParam) &&
                this.isValidUTMMedium(utmMediumParam)
            ) {
                this.storeEngagement(utmCampaignParam, utmSourceParam, utmMediumParam, gclid, /* expiration, in days */ 365);
            } else if (this.isValidMCCID(mccid)) {
                this.storeMCCIDEngagement(mccid, 365);
            }
        },
        /**
         * Convert our saved engagement data to Shopify cart attributes
         * @param {Object}  engagement Engagement object from our cookie.
         * @return {Object} Engagement object to be sent to Shopify's cart attribute input fields.
         */
        engagementToAttribs: function (engagement) {
            return {
                "utm_campaign": engagement.id,
                "utm_source": engagement.src,
                "utm_medium": engagement.medium,
                "created_at": engagement.created_at,
                "gclid": engagement.gclid,
                "mc_cid": engagement.mccid
            };
        },
        /**
         * Handles injecting cart attribute input fields into the Shopify Cart form.
         * @param {Element} cartForm   Shopify Cart form's Document Element.
         * @param {Object}  engagement Engagement object from our cookie.
         */
        injectCartAttributes: function (cartForm, engagement) {
            var attribs = this.engagementToAttribs(engagement);
            var p = this.createAttributeParagraphElement();
            for (var attribName in attribs) {
                if (attribs.hasOwnProperty(attribName)) {
                    var input = this.createAttributeInputField(attribName, attribs[attribName]);
                    p.appendChild(input);
                }
            }
            cartForm.appendChild(p);
        },
        /**
         * Checks if "Do Not Track" is enabled.
         * @return {Boolean} Whether the browser has "Do Not Track" enabled.
         */
        isDoNotTrack: function () {
            if (navigator.doNotTrack === "1") {
                return true;
            }

            if (navigator.msDoNotTrack === "1") {
                return true;
            }

            return false;
        },
        /**
         * Gets the current unix timestamp.
         * @return {Number} The timestamp in seconds.
         */
        getUnixTimestamp: function () {
            return Math.round((new Date()).getTime() / 1000);
        },
        /**
         * Gets the value of a query parameter.
         * @param {String} name     The param name.
         * @return {String|null}    The param value.
         */
        getParameter: function (name) {
            name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
            var results = regex.exec(location.search);

            return results === null ? null : decodeURIComponent(results[1].replace(/\+/g, " "));
        },
        /**
         * Checks if the "utm_campaign" value is valid.
         * @param {String} utmCampaignParam The param value.
         * @return {Boolean}                Whether the value is valid.
         */
        isValidUTMCampaign: function (utmCampaignParam) {
            if (!utmCampaignParam) {
                return false;
            }

            var regex = new RegExp("^[a-zA-Z0-9]{10,12}$"); // unique_id for campaigns is 10, ads is 12

            return utmCampaignParam.search(regex) === -1 ? false : true;
        },
        /**
         * Checks if the "utm_source" value is valid.
         * @param {String} utmSourceParam   The param value.
         * @return {Boolean}                Whether the value is valid.
         */
        isValidUTMSource: function (utmSourceParam) {
            if (!utmSourceParam) {
                return false;
            }

            var regex = new RegExp("^mailchimp$", "i");

            return utmSourceParam.search(regex) === -1 ? false : true;
        },
        /**
         * Checks if the "utm_medium" value is valid.
         * @param {String} utmMediumParam   The param value.
         * @return {Boolean}                Whether the value is valid.
         */
        isValidUTMMedium: function (utmMediumParam) {
            if (!utmMediumParam) {
                return false;
            }

            var regex = new RegExp("^(campaign|ad)$", "i");

            return utmMediumParam.search(regex) === -1 ? false : true;
        },
        /**
         * Checks if the "mc_cid" value is valid.
         * @param {String} mccid            The param value.
         * @return {Boolean}                Whether the value is valid.
         */
        isValidMCCID: function (mccid) {
            if (!mccid) {
                return false;
            }

            var regex = new RegExp("^[a-zA-Z0-9]{10,12}$"); // unique_id for campaigns is 10, ads is 12

            return mccid.search(regex) === -1 ? false : true;
        },
        /**
         * Gets engagement objects from the stored cookie.
         * @return {Object[]} An array of engagement objects.
         */
        getEngagements: function () {
            var cookie = this.readCookie("mc_track");
            var engagements = JSON.parse(decodeURIComponent(cookie));

            return engagements !== null ? engagements : [];
        },
        /**
         * Gets engagement objects from the stored cookie, sorted by creation time.
         * @return {Object[]} An array of engagement objects.
         */
        getEngagementsSortedByCreatedAt: function () {
            var engagements = this.getEngagements();
            return engagements.sort(function (a, b) {return b.created_at - a.created_at;});
        },
        /**
         * Gets the most recent engagement object.
         * @return {Object|null} An engagement object.
         */
        getMostRecentEngagement: function () {
            var engagements = this.getEngagementsSortedByCreatedAt();
            return engagements.length > 0 ? engagements[0] : null;
        },
        /**
         * Gets whether an engagement with the provided id is already stored.
         * @param {String} id   Engagment id to be checked.
         * @return {Boolean}    Whether the engagement is already stored.
         */
        hasStoredEngagement: function (id) {
            var engagements = this.getEngagements();
            return engagements.filter(function (obj) {return obj.id === id;}).length === 0 ? false : true;
        },
        /**
         * Returns whether an mc_cid is already stored as an engagement.
         *
         * @param {String} mccid    The mc_cid.
         *
         * @return {boolean}        Whether the engagement is already stored.
         */
        hasStoredMCCIDEngagement: function (mccid) {
            return this.getEngagements().filter(function (obj) {return obj.mccid && obj.mccid === mccid;}).length === 0 ? false : true;
        },
        /**
         * Stores an engagement object in the cookie.
         * @param {String} id           The engagement id / utm_campaign.
         * @param {String} source       The utm_source.
         * @param {String} medium       The utm_medium.
         * @param {String} gclid        The gclid.
         * @param {number} expiration   Number of days before this should expire.
         */
        storeEngagement: function (id, source, medium, gclid, expiration) {
            if (!this.hasStoredEngagement(id)) {
                var engagements = this.getEngagements();

                var engagementObj = this.generateEngagementObject(id, source, medium, gclid, null);
                engagements.push(engagementObj);

                // unix timestamp of ~2 months ago
                var twoMonthsAgo = this.getUnixTimestamp() - 60 * 60 * 24 * 60;

                // remove engagements older than 2 months
                var recentEngagements = engagements.filter(function (obj) {
                    return obj.created_at > twoMonthsAgo;
                });

                this.createCookie("mc_track", JSON.stringify(recentEngagements), expiration);
            }
        },
        /**
         * Stores an mc_cid engagement.
         *
         * @param {String} mccid        The mc_cid.
         * @param {number} expiration   Expiration, in days.
         */
        storeMCCIDEngagement: function (mccid, expiration) {
            if (this.hasStoredMCCIDEngagement(mccid)) {
                return;
            }

            var engagements = this.getEngagements();

            var engagementObj = this.generateEngagementObject(null, null, null, null, mccid);
            engagements.push(engagementObj);

            // unix timestamp of ~2 months ago
            var twoMonthsAgo = this.getUnixTimestamp() - 60 * 60 * 24 * 60;

            // remove engagements older than 2 months
            var recentEngagements = engagements.filter(function (obj) {
                return obj.created_at > twoMonthsAgo;
            });

            this.createCookie("mc_track", JSON.stringify(recentEngagements), expiration);
        },
        /**
         * Generates an engagement object.
         * @param {String} id           The engagement id / utm_campaign value.
         * @param {String} source       The utm_source value.
         * @param {String} medium       The utm_medium value.
         * @param {String} gclid        The gclid value.
         * @param {String} mccid        The mc_cid value.
         * @return {Object}             The generated engagement object.
         */
        generateEngagementObject: function (id, source, medium, gclid, mccid) {
            return {
                "id": id,
                "src": source,
                "medium": medium,
                "gclid": gclid,
                "mccid": mccid,
                "created_at": this.getUnixTimestamp()
            };
        },
        /**
         * Creates a cookie.
         * @param {String} name             The cookie name.
         * @param {String} value            The cookie value.
         * @param {Number} expirationDays   The cookie's expiration time, in days.
         */
        createCookie: function (name, value, expirationDays) {
            var cookie_value = encodeURIComponent(value) + ";";

            // set expiration
            if (expirationDays !== null) {
                var expirationDate = new Date();
                expirationDate.setDate(expirationDate.getDate() + expirationDays);
                cookie_value += " expires=" + expirationDate.toUTCString() + ";";
            }

            // set path
            cookie_value += "path=/";

            document.cookie = name + "=" + cookie_value;
        },
        /**
         * Retrieves a cookie value.
         * @param {String} name     The cookie name.
         * @return {String|null}    The cookie value.
         */
        readCookie: function (name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(";");

            for (var i = 0; i < ca.length; i++) {
                var c = ca[i];

                while (c.charAt(0) === " ") {
                    c = c.substring(1, c.length);
                }

                if (c.indexOf(nameEQ) === 0) {
                    return c.substring(nameEQ.length, c.length);
                }
            }

            return null;
        },
        /**
         * Retrieves the Shopify Cart form from the DOM.
         * @return {Element|null} The Shopify cart form element.
         */
        getCartForm: function () {
            return document.querySelector("form[action='/cart']");
        },
        /**
         * Creates a hidden Input Field element for cart attribute injection.
         * @param {String} name     The "name" value for the input field.
         * @param {String} value    The "value" value for the input field.
         * @return {Element}        The created input field element.
         */
        createAttributeInputField: function (name, value) {
            var input = document.createElement("input");
            input.type = "hidden";
            input.name = "attributes[" + name + "]";
            input.value = value;

            return input;
        },
        /**
         * Creates a Paragraph element for Shopify's custom cart attributes.
         * @return {Element}        The created paragraph element.
         */
        createAttributeParagraphElement: function () {
            var p = document.createElement("p");
            p.setAttribute("class", "cart-attribute__field");

            return p;
        },
        /**
         * Save the engagement using the Shopify Ajax API. Eats errors.
         * @param {Object} engagement Engagement object from our cookie.
         */
        postCartAttributes: function (engagement) {
            var attribs = this.engagementToAttribs(engagement);
            try {
                var req = new XMLHttpRequest();
                req.open("POST", "/cart/update.js", true);
                req.setRequestHeader("Content-Type", "application/json");
                req.send(JSON.stringify({attributes: attribs}));
            } catch (send_error) {
                console.warn("Unable to set attribution params in Shopify: " + send_error.message);
            }
        },

        updateCustomerSession: function () {
            var customer_session_id = this.readCookie("mc_customer_session_id");
            if (customer_session_id) {

                var data = {
                    attributes: {
                        customer_session_id: customer_session_id
                    }
                };

                try {
                    var req = new XMLHttpRequest();
                    req.open("POST", "/cart/update.js", true);
                    req.setRequestHeader("Content-Type", "application/json");
                    req.send(JSON.stringify(data));
                } catch (send_error) {
                    console.warn("Unable to set attribution params in Shopify: " + send_error.message);
                }
            }
        }
    };

    if (window.$mcSite === undefined || window.$mcSite.shopify_attribution_cookie === undefined) {
        return;
    }

    var module = window.$mcSite.shopify_attribution_cookie;

    if (module.installed === true) {
        return;
    }

    module.installed = true;

    if (conversion.isDoNotTrack()) {
        return;
    }

    conversion.processParameters();

    // wait a sec for the attribution call to be made
    setTimeout(function () {
        conversion.updateCustomerSession();
    }, 3000);

    var engagement = conversion.getMostRecentEngagement();
    if (engagement === null || engagement === undefined) {
        return;
    }

    var cartForm = conversion.getCartForm();
    if (cartForm === null) {
        conversion.postCartAttributes(engagement);
    } else {
        conversion.injectCartAttributes(cartForm, engagement);
    }
}());
(function () {
    if (window.$mcSite === undefined || window.$mcSite.popup_form === undefined) {
        return;
    }

    if (window.location.href.indexOf("checkout.shopify") >= 0) {
        return;
    }

    var scripts = document.getElementsByTagName("script");
    for (var i = 0; i < scripts.length; i++) {
        // look for src containing the old embed.js code and bail if it exists
        if (scripts[i].getAttribute("src") === "//s3.amazonaws.com/downloads.mailchimp.com/js/signup-forms/popup/embed.js" || scripts[i].getAttribute("src") === "//downloads.mailchimp.com/js/signup-forms/popup/embed.js") {
            return;
        }
    }

    var module = window.$mcSite.popup_form;

    if (module.installed === true) {
        return;
    }

    if (!module.settings) {
        return;
    }

    var settings = module.settings;

    if (!settings.base_url || !settings.uuid || !settings.list_id || settings.skip_install === "1") {
        return;
    }

    var script = document.createElement("script");

    script.src = "//downloads.mailchimp.com/js/signup-forms/popup/unique-methods/embed.js";
    script.type = "text/javascript";
    script.onload = function () {
        if (window.dojoRequire) {
            window.dojoRequire(["mojo/signup-forms/Loader"], function (L) {
                L.start({
                    "baseUrl": settings.base_url,
                    "uuid": settings.uuid,
                    "lid": settings.list_id,
                    "uniqueMethods": true,
                    "f_id": settings.f_id
                });
            });
        }
    };

    document.body.appendChild(script);

    window.$mcSite.popup_form.installed = true;
}());
(function () {
    var module = window.$mcSite.amped_forms;

    if (module.installed === true) {
        return;
    }

    if (!module.settings) {
        return;
    }

    var settings = module.settings;

    if (!settings.uid) {
        return;
    }

    window.$mcSite.runIfOptedIn(function () {
        var script = document.createElement("script");

        var fixedUrl = settings.src.replace("\\/", "/");

        script.src = fixedUrl + settings.uid + "?site=" + settings.site_unique_id;
        script.type = "text/javascript";

        document.body.appendChild(script);
    }, [
        "preferencesProcessingAllowed",
        "analyticsProcessingAllowed",
        "marketingAllowed"
    ]);
}());
(function () {
    var module = window.$mcSite.pixel;

    if (module.installed === true) {
        return;
    }

    if (!module.settings) {
        return;
    }

    var settings = module.settings;

    if (!settings.domain || !settings.version || !settings.apiUrl) {
        return;
    }

    var sdkUrl = "https://" + settings.domain + "/assets/pixel-reporting-sdk/" + settings.version + "/pixel-reporting-sdk.js";

    var context = {
        mailchimpAudienceId: settings.context_mailchimpAudienceId,
        mailchimpStoreId: settings.context_mailchimpForeignStoreId,
        mailchimpConnectedSiteId: settings.context_publicConnectedSiteId,
        mailchimpUserId: settings.context_mailchimpUserId
    };

    var script = document.createElement("script");
    script.type = "module";
    script.textContent =
        'import pixel from "' + sdkUrl + '";' +
        "window.$mcSite.pixel.api = pixel;";

    window.$mcSite.runIfOptedIn(function () {
        Object.defineProperty(module, "api", {
            set: function (pixel) {
                Object.defineProperty(module, "api", { value: pixel, writable: true });

                var disableMailchimpPixelAutoTrack =
                    typeof window.disable_mailchimp_pixel_autotrack !== "undefined" &&
                    window.disable_mailchimp_pixel_autotrack === true;

                var autoTrack = disableMailchimpPixelAutoTrack ? false : settings.autoTrack === "true";

                pixel.init({
                    apiUrl: settings.apiUrl.replace(/\\\//g, "/"),
                    autoTrack: autoTrack,
                    referenceSystem: settings.context_referenceSystem,
                    context: context
                });

                module.installed = true;
            },
            configurable: true
        });

        document.body.appendChild(script);
    }, [
        "preferencesProcessingAllowed",
        "analyticsProcessingAllowed",
        "marketingAllowed"
    ]);
}());
"

**Custom Pixels / Customer Events**

I dont have access to custoerm events so i odnt know

**Theme "additional scripts" & Preferences**

No additional scripts/preferences at the online store -> preferences path, might need a btter path

**Google Tag Manager / other tag manager**

Does not point at google tag manager

**Mailchimp side — where the popup is actually configured**

I get to mailchimp -> audience -> signup source -> popup form but i dont see anyoen added since 2025
