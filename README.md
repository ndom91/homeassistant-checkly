# Checkly

Homeassistant integration to add sensors for your Checkly API and Browser checks!

> Heavily based off of the [UptimeRobot](https://github.com/home-assistant/core/tree/dev/homeassistant/components/uptimerobot) Integration ❤️

## 🏗 Installation

1. Clone the repository into your `/custom_components` directory.

```bash
$ cd <config_dir>/custom_components
$ git clone https://github.com/ndom91/homeassistant-checkly.git
```

2. Add this to your sensor configuration. For example, in `configuration.yaml`.

```yaml
sensor:
  platform: checkly
```

## ⚙ Configuration

Once you've cloned the sensor integration into your `custom_components` directory, you've got to add a Checkly API key. These can be generated in the [API Keys](https://app.checklyhq.com/settings/user/api-keys) area of the settings.  Then add this API key as the `token` parameter to your sensor configuration.

```yaml
sensor:
  platform: checkly
  token: cu_abc123
```

Now you should have sensors for the passing/failing status for each of your checks and groups available to you in your HomeAssistant. You can create automations based off of these, or just display them on your dashboard.

## 👷 Contributing

We are happy to accept any and all contributions.

## 📝 License

MIT
