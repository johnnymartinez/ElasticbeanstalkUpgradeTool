#!/usr/bin/env node

const AWS = require('aws-sdk');
AWS.config.update({ region: "us-west-2" });
AWS.config.setPromisesDependency(require('bluebird'));
const elasticbeanstalk = new AWS.ElasticBeanstalk();
const _ = require('lodash');

upgradePlatform('ahj-scope-dev-2-jm-test');


async function getLatestPlatformVersion() {
    platforms = await elasticbeanstalk.listPlatformVersions().promise();
    nodePlatforms = _.filter(platforms.PlatformSummaryList, { PlatformCategory: "Node.js" });
    nodePlatforms = _.sortBy(nodePlatforms, ["OperatingSystemVersion", "PlatformArn"]);
    return nodePlatforms[nodePlatforms.length - 1].PlatformArn;
}

async function upgradePlatform(envName) {
    var nodeVersions = null;
    let latestPlatform = await getLatestPlatformVersion();

    let response = await elasticbeanstalk.describeConfigurationOptions({ PlatformArn: latestPlatform }).promise()

    data = response.Options;

    data.forEach(function (option) {
        if (option.Namespace == "aws:elasticbeanstalk:container:nodejs" && option.Name == "NodeVersion") {
            nodeVersions = option.ValueOptions;
        }
    })

    response = await elasticbeanstalk.describeEnvironments({ "EnvironmentNames": [envName] }).promise();

    if (!response || !response.Environments || response.Environments.length == 0) {
        console.log(`${envName} not found`);
        return false;
    }

    let environment = response.Environments[0];

    const OptionSettings = [];

    let nodeVersion = null;

    let reponse = await elasticbeanstalk.describeConfigurationSettings({ ApplicationName: environment.ApplicationName, EnvironmentName: environment.EnvironmentName }).promise();

    // console.log(util.inspect(response, { depth: 5 }));
    config = reponse.ConfigurationSettings[0];

    config.OptionSettings.forEach(function (option) {
        console.log(option);
        if (option.Namespace == "aws:elasticbeanstalk:container:nodejs" && option.OptionName == "NodeVersion") {
            nodeVersion = option.Value;
        }
    });

    // TODO only grabbing first character doesn't work for node 10
    // nodeVersion.split('.') Array(10, 1, 1)
    // nodeVersion[0]
    let majorVersion = nodeVersion.split('.')[0]

    newVersion = _.findLast(nodeVersions, function (o) { return o.split('.')[0] == majorVersion });

    OptionSettings.push({
        Namespace: "aws:elasticbeanstalk:container:nodejs",
        OptionName: "NodeVersion",
        Value: newVersion
    })

    console.log(OptionSettings);
    elasticbeanstalk.updateEnvironment({
        ApplicationName: environment.ApplicationName,
        EnvironmentName: environment.EnvironmentName,
        PlatformArn: latestPlatform,
        OptionSettings: OptionSettings,
    }, function (err, resp) {
        console.log(err);
        console.log(resp);
    })
}
