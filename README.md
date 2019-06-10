## 쿠버네티스 kubernetes (k8s)

컨테이너 오케스트레이션을 위한 도구로 구글이 개발하고 현재는 리눅스 재단에서 관리하고 있다.

# install helm
   kubernetes의 패키지 매니저로서 [여기](https://helm.sh)에서 받을 수 있다.

1. ha-etcd-cluster
   - 고가용성을 목표로 쿠버네티스의 상태저장 클러스터를 다중화하는 예제입니다.

2. job & cronjob
   - 쿠버네티스의 내부에서 파이썬 스크립트를 job으로 동작시키는 예제입니다.

3. namespace
   - 쿠버네티스의 컨텍스트 분리를 위한 네임스페이스 생성을 하는 예제입니다.

4. service
   - 쿠버네티스의 서비스를 생성하는 예제 입니다.

5. Daemonset
   - 준비중입니다.
 

# 쿠버네티스 컴포넌트

클러스터 : 쿠버네티스의 시스템을 구성하는 다양한 기능들을 실행시키는 컴퓨터 저장소 네트워크의 자원이다.

- 노드/미니온 : 베어메탈 머신 가상머신 일 수 있다. 노드는 포드를 실행시키며 
각 쿠버네티스 노드들은 서로 kubelet이나 kube proxy 여러 쿠버네티스  컴포넌트로 구성되있다.
- etcd : 쿠버네티스의 클러스터의 정보를 가지고 있는 컴포넌트
- kube-apiserver : 쿠버네티스의 API
- secret : 자격증명 및 토큰 정보를 저장하는 작은 객체
- master : 쿠버네티스의 컨트롤 플레인으로 클러스터를 관리하는 유닛이다 
마스터는 API서버 와 프록시 스케줄러 등등 여러 컴포넌트로 구현된다,
- pod : 쿠버네티스의 작업 단위로서 포드에는 한 개 또는 여러 개의 컨테이너가
 들어있다 포드의 컨테이너는 동일한 IP주소와 포트공간을 가지고 있으며 로컬호스트를 사용하거나 표준 IPC를 사용해 서로 통신한다. 또한 포드를 호스팅하는 노드의 저장소에도 접근이 가능하고 저장소에서 컨테이너로 마운트될 수 있다.

 더욱 자세한건 [여기](https://kubernetes.io/ko/docs/setup/cluster-large/)에서 확인할 수 있습니다.

## 쿠버네티스의 클러스터 구성

아래와 같은 명령어를 이용하여 쿠버네티스를 구성할 수 있다.

```bash
    kubeadm init --apiserver-advertise-address [IP]  // 마스터 구축

    sudo sysctl net.bridge.bridge-nf-call-iptables=1 // 가상화 네트워크 옵션 켜기

    kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')" // cni 

```

### 쿠버네티스 고가용성 구축 

### 1. 노드 안정화

```bash
    systemctl enable docker
    systemctl enable kubelet 
```
### 2. 클러스터 상태 보호 

쿠버네티스의 모든 클러스터의 상태의 정보는 etcd에서 관리한다
따라서 더 높은 신뢰와 중복을 확보하려면 홀수개의 etcd를 운용하는것이 바람직하다

이를 구성하기 위하여 여러가지 방법이 있는데, CoreOS에서 제공하는 etcd-operator를 사용하여 구성할 수 있다.

### 3. 마스터 참여하기

```bash
    kubeadm join [token] [ip] //
```

만약 조인 커맨드를 잃어버렸을 경우 마스터 노드에서 아래의 명령어를 입력하여 다시 받을 수 있다.

```bash
    kubeadm token create --print-join-command
```


### 4. 파이썬 REST CUSTOM API를 작성한다

http://github.com/kubernetes-client/python 를 기반으로 작성되었다

```bash
    pip install kubernetes
```
아래에 API 명세가 설명되어 있다.

https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md 


아래 예제 에서는 kubenetes api 서버상에서 동작하는 파드와 모든 네임스페이스를 조회하는 것을 다뤄보겠다

```python
# all_pod_view_namespace.py
from kubernetes import client

config.load_kube_config() # 현재 실행중인 kubectl의 설정 정보를 읽어서 연결

v1 = client.CoreV1Api()

print("Listing pods with their IPs:")

ret = v1.list_pod_for_all_namespace()

for i in ret.items:
    print ("%s \t %s \t %s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


v1 = CoreV1Api()

v1 = kubernetes.client.AdmissionregistrationV1beta1Api(kubenetes.client.Apiclient(config))

```

위와 같이 kubectl proxy를 이용한 쿠버네티스 엔드포인트를 지정하고 각 언어에 구현된 API
로 클러스터의 상태 관리 및 서비스 추가 배포가 가능하다.


#### 참고자료

[카카오 클라우드](https://www.slideshare.net/openstack_kr/openinfra-days-korea-2018-day-2-e5-mesos-to-kubernetes-cloud-native)

[쿠버네티스 공식 문서](https://k8s.io)

[불륨 스토리지 매니저 툴](https://github.com/heketi/heketi)