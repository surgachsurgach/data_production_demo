import boto3

class Cluster:
    def __init__(self, region: str = "ap-northeast-2", spot: bool = True) -> None:
        self.region = region
        self.pem_key = "your-ec2-key-name"
        self.emr_client = boto3.client("emr", region_name=self.region)

    # TODOs: need to set configurations below.
    # In this time, I created EMR Cluster and tested spark application by adding steps on AWS console
    # I referenced material below
    # boto3 python sdk guide
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr.html#EMR.Client.run_job_flow
    # AWS EMR configuration guide
    # https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-configure-apps.html
    # Instead, we can simply use Airflow EmrCreateJobFlowOperator
    # https://airflow.apache.org/docs/apache-airflow-providers-amazon/stable/operators/emr.html#create-emr-job-flow-with-automatic-steps
    def create(self, **kwargs):
        response = self.emr_client.run_job_flow(
            Name='string',
            LogUri='string',
            LogEncryptionKmsKeyId='string',
            AdditionalInfo='string',
            AmiVersion='string',
            ReleaseLabel='string',
            Instances={
                'MasterInstanceType': 'string',
                'SlaveInstanceType': 'string',
                'InstanceCount': 123,
                'InstanceFleets': [
                    {
                        'Name': 'string',
                        'InstanceFleetType': 'MASTER' | 'CORE' | 'TASK',
                        'TargetOnDemandCapacity': 123,
                        'TargetSpotCapacity': 123,
                        'InstanceTypeConfigs': [
                            {
                                'InstanceType': 'string',
                                'WeightedCapacity': 123,
                                'BidPrice': 'string',
                                'BidPriceAsPercentageOfOnDemandPrice': 123.0,
                                'EbsConfiguration': {
                                    'EbsBlockDeviceConfigs': [
                                        {
                                            'VolumeSpecification': {
                                                'VolumeType': 'string',
                                                'Iops': 123,
                                                'SizeInGB': 123
                                            },
                                            'VolumesPerInstance': 123
                                        },
                                    ],
                                    'EbsOptimized': True | False
                                },
                                'Configurations': [
                                    {
                                        'Classification': 'string',
                                        'Configurations': {'... recursive ...'},
                                        'Properties': {
                                            'string': 'string'
                                        }
                                    },
                                ]
                            },
                        ],
                        'LaunchSpecifications': {
                            'SpotSpecification': {
                                'TimeoutDurationMinutes': 123,
                                'TimeoutAction': 'SWITCH_TO_ON_DEMAND' | 'TERMINATE_CLUSTER',
                                'BlockDurationMinutes': 123,
                                'AllocationStrategy': 'capacity-optimized'
                            },
                            'OnDemandSpecification': {
                                'AllocationStrategy': 'lowest-price'
                            }
                        }
                    },
                ],
                'Ec2KeyName': self.pem_key,
                'Placement': {
                    'AvailabilityZone': 'string',
                    'AvailabilityZones': [
                        'string',
                    ]
                },
                'KeepJobFlowAliveWhenNoSteps': True | False,
                'TerminationProtected': True | False,
                'HadoopVersion': 'string',
                'Ec2SubnetId': 'string',
                'Ec2SubnetIds': [
                    'string',
                ],
                'EmrManagedMasterSecurityGroup': 'string',
                'EmrManagedSlaveSecurityGroup': 'string',
                'ServiceAccessSecurityGroup': 'string',
                'AdditionalMasterSecurityGroups': [
                    'string',
                ],
                'AdditionalSlaveSecurityGroups': [
                    'string',
                ]
            },
            Steps=[
                {
                    'Name': 'string',
                    'ActionOnFailure': 'TERMINATE_JOB_FLOW' | 'TERMINATE_CLUSTER' | 'CANCEL_AND_WAIT' | 'CONTINUE',
                    'HadoopJarStep': {
                        'Properties': [
                            {
                                'Key': 'string',
                                'Value': 'string'
                            },
                        ],
                        'Jar': 'string',
                        'MainClass': 'string',
                        'Args': [
                            'string',
                        ]
                    }
                },
            ],
            BootstrapActions=[
                {
                    'Name': 'string',
                    'ScriptBootstrapAction': {
                        'Path': 'string',
                        'Args': [
                            'string',
                        ]
                    }
                },
            ],
            SupportedProducts=[
                'string',
            ],
            NewSupportedProducts=[
                {
                    'Name': 'string',
                    'Args': [
                        'string',
                    ]
                },
            ],
            Applications=[
                {
                    'Name': 'string',
                    'Version': 'string',
                    'Args': [
                        'string',
                    ],
                    'AdditionalInfo': {
                        'string': 'string'
                    }
                },
            ],
            Configurations=[
                {
                    'Classification': 'string',
                    'Configurations': {'... recursive ...'},
                    'Properties': {
                        'string': 'string'
                    }
                },
            ],
            VisibleToAllUsers=True | False,
            JobFlowRole='string',
            ServiceRole='string',
            Tags=[
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            SecurityConfiguration='string',
            AutoScalingRole='string',
            ScaleDownBehavior='TERMINATE_AT_INSTANCE_HOUR' | 'TERMINATE_AT_TASK_COMPLETION',
            CustomAmiId='string',
            EbsRootVolumeSize=123,
            RepoUpgradeOnBoot='SECURITY' | 'NONE',
            KerberosAttributes={
                'Realm': 'string',
                'KdcAdminPassword': 'string',
                'CrossRealmTrustPrincipalPassword': 'string',
                'ADDomainJoinUser': 'string',
                'ADDomainJoinPassword': 'string'
            },
            StepConcurrencyLevel=123,
            ManagedScalingPolicy={
                'ComputeLimits': {
                    'UnitType': 'InstanceFleetUnits' | 'Instances' | 'VCPU',
                    'MinimumCapacityUnits': 123,
                    'MaximumCapacityUnits': 123,
                    'MaximumOnDemandCapacityUnits': 123,
                    'MaximumCoreCapacityUnits': 123
                }
            },
            PlacementGroupConfigs=[
                {
                    'InstanceRole': 'MASTER' | 'CORE' | 'TASK',
                    'PlacementStrategy': 'SPREAD' | 'PARTITION' | 'CLUSTER' | 'NONE'
                },
            ]
        )

        self.id = response['JobFlowId']
        print(f"Initiated EMR cluster with ID: {self.id}...")

        return self.id

    @staticmethod
    def terminate(self, **kwargs) -> None:
        if not self.id:
            raise ValueError("There is no cluster to terminate!")

        print(f"Terminate EMR cluster with ID: {self.id}...")
        cluster_id = kwargs['ti'].xcom_pull(kwargs["create_task_id"])
        self.emr_client.set_termination_protection(JobFlowIds=[cluster_id], TerminationProtected=False)
        self.emr_client.terminate_job_flows(JobFlowIds=[cluster_id])
