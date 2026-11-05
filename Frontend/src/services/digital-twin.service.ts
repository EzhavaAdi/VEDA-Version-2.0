/**
 * VEDA V2 — Digital Twin API service
 */
import { api } from './api'
import type { Asset3D, SceneState } from '../types/digital-twin'

export const digitalTwinService = {
  listAssets: () =>
    api.get<Asset3D[]>('/digital-twin/assets/'),

  getAsset: (assetId: string) =>
    api.get<Asset3D>(`/digital-twin/assets/${assetId}/`),

  getSceneState: (assetId: string, orderId?: string) => {
    const qs = orderId ? `?order_id=${orderId}` : ''
    return api.get<SceneState>(`/digital-twin/assets/${assetId}/scene/${qs}`)
  },
}
