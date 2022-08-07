# Checkly

[Home Assistant](https://www.home-assistant.io/) integration to add sensors for your Checkly API and Browser checks!

> Heavily based off of the [UptimeRobot](https://github.com/home-assistant/core/tree/dev/homeassistant/components/uptimerobot) Integration ❤️

## 🏗 Installation

1. Clone the repository into your `/custom_components` directory.

```bash
$ cd <config_dir>/custom_components
$ git clone https://github.com/ndom91/homeassistant-checkly.git checkly
```

Once you've cloned this into the `custom_components` directory, the rest of the configuration can be done in the Home Assistant UI.

## ⚙ Configuration

To add your Checks to Home Assistant, you have to add the custom integration as follows.

1. In Home Assistant, go to `Settings` -> `Devices & Services`
2. Under the `Integrations` tab, click `Add Integration` and search for `Checkly` in the list of available options.
3. When selected, a pop-up will open asking you for your Checkly API Token and Account ID. These can both be found in the [Settings](https://app.checklyhq.com/settings/account/general) area of the Checkly Webapp.
4. Once confirmed, you will be shown a list of all of your Checks at which point you can assign them to "Areas", if you wish.

Now you should have sensors for the `passing`/`failing` state for each of your checks available in your Home Assistant. You can now create automations based off of these, or just display them on your dashboard. 

## 👷 Contributing

We are happy to accept any and all contributions.

## 📝 License

MIT
